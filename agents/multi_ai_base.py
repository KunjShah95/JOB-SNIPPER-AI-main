from agents.advanced_agent_base import AdvancedAgentBase
from utils.config import GEMINI_API_KEY, MISTRAL_API_KEY
import time
import logging
from typing import Callable, List, Optional, Dict, Any
import asyncio
from threading import Lock

import importlib.util

# Import AI libraries based on availability
if importlib.util.find_spec("google.generativeai") is not None:
    GENAI_AVAILABLE = True
else:
    GENAI_AVAILABLE = False

# Note: Mistral import is done dynamically in setup_ai_clients to handle errors better


class MultiAIAgent(AdvancedAgentBase):
    """Base class for agents that support multiple AI providers simultaneously, with advanced features"""

    def __init__(
        self,
        name,
        use_gemini=True,
        use_mistral=True,
        return_mode="aggregate",
        verbose=False,
        fallback_to_fallback=True,
        prompt_template: Optional[str] = None,
        provider_priority: Optional[List[str]] = None,
        max_retries: int = 1,
        postprocess_hook: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        cache_enabled: bool = False,
        provider_settings: Optional[Dict[str, dict]] = None,
        rate_limit_per_minute: int = 0,
        user_context: Optional[Dict[str, Any]] = None,
    ):
        """
        use_gemini: bool - whether to use Gemini
        use_mistral: bool - whether to use Mistral
        return_mode: str - 'aggregate', 'compare', or 'dict'
        verbose: bool - enable verbose logging
        fallback_to_fallback: bool - fallback to static response if all providers fail
        prompt_template: str - optional template for prompts
        provider_priority: list - order of provider usage
        max_retries: int - number of retries per provider
        postprocess_hook: callable - function to postprocess responses
        cache_enabled: bool - enable in-memory caching of prompt->response
        provider_settings: dict - per-provider custom settings (e.g., model, temperature)
        rate_limit_per_minute: int - max requests per minute (0 = unlimited)
        user_context: dict - user/session context for personalization or logging
        """
        super().__init__(
            name=name, enable_caching=cache_enabled, max_retries=max_retries
        )
        self.gemini_available = False
        self.mistral_available = False
        self.gemini_model = None
        self.mistral_client = None
        self.mistral_model_name = None
        self.use_gemini = use_gemini
        self.use_mistral = use_mistral
        self.return_mode = return_mode
        self.verbose = verbose
        self.prompt_template = prompt_template
        self.provider_priority = provider_priority or ["gemini", "mistral"]
        self.postprocess_hook = postprocess_hook
        self.provider_settings = provider_settings or {}
        self.rate_limit_per_minute = rate_limit_per_minute
        self._rate_limit_lock = Lock()
        self._rate_limit_timestamps = []
        self.usage_stats = {"total_requests": 0, "per_provider": {}}
        self.user_context = user_context or {}
        self.setup_ai_clients()

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Default implementation of abstract process method from Agent base class.

        This method provides a default implementation that child classes can override.
        It converts input_data to a prompt and uses the AI generation capabilities.

        Args:
            input_data: Dictionary containing the data to process

        Returns:
            Dictionary containing the processed results
        """
        try:
            # Default behavior: convert input to string and generate response
            if isinstance(input_data, dict):
                # Try to extract meaningful prompt from input_data
                if "prompt" in input_data:
                    prompt = input_data["prompt"]
                elif "data" in input_data:
                    prompt = f"Process this data: {input_data['data']}"
                else:
                    prompt = f"Process this input: {input_data}"
            else:
                prompt = f"Process this input: {input_data}"

            # Generate response using AI
            response = self.generate_ai_response(prompt)

            # Return structured result
            return {
                "success": True,
                "result": response,
                "input": input_data,
                "agent": self.name,
            }

        except Exception as e:
            # Return error response
            return {
                "success": False,
                "error": str(e),
                "input": input_data,
                "agent": self.name,
            }

    def setup_ai_clients(self):
        """Setup both Gemini and Mistral clients if available"""
        # Setup Gemini
        if self.use_gemini and GENAI_AVAILABLE and GEMINI_API_KEY:
            try:
                import google.generativeai as genai

                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel("gemini-2.5-pro")
                self.gemini_available = True
                if self.verbose:
                    logging.info("Gemini 2.5 Pro client initialized.")
            except Exception as e:
                logging.warning(f"Failed to setup Gemini: {e}")
        # Setup Mistral
        if self.use_mistral:
            try:
                from mistralai import Mistral

                self.mistral_client = Mistral(api_key=MISTRAL_API_KEY)
                self.mistral_model_name = "mistral-large-latest"
                self.mistral_available = True
                if self.verbose:
                    logging.info("Mistral client initialized.")
            except ImportError as ie:
                logging.warning(f"Mistral client not available: {ie}")
            except Exception as me:
                logging.warning(f"Failed to setup Mistral client: {me}")
        if not (self.gemini_available or self.mistral_available):
            logging.warning("No AI providers available, will use fallback responses.")

    def format_prompt(self, prompt: str, **kwargs) -> str:
        if self.prompt_template:
            return self.prompt_template.format(prompt=prompt, **kwargs)
        return prompt

    def _cache_key(self, provider, prompt):
        return f"{provider}:{prompt}"

    def _check_rate_limit(self):
        if self.rate_limit_per_minute > 0:
            with self._rate_limit_lock:
                now = time.time()
                # Remove timestamps older than 60 seconds
                self._rate_limit_timestamps = [
                    t for t in self._rate_limit_timestamps if now - t < 60
                ]
                if len(self._rate_limit_timestamps) >= self.rate_limit_per_minute:
                    raise Exception(
                        f"Rate limit exceeded: {self.rate_limit_per_minute} requests per minute"
                    )
                self._rate_limit_timestamps.append(now)

    def _update_usage_stats(self, provider, success=True):
        self.usage_stats["total_requests"] += 1
        if provider not in self.usage_stats["per_provider"]:
            self.usage_stats["per_provider"][provider] = {"success": 0, "fail": 0}
        if success:
            self.usage_stats["per_provider"][provider]["success"] += 1
        else:
            self.usage_stats["per_provider"][provider]["fail"] += 1

    def get_health_status(self):
        health = {}
        for provider in self.provider_priority:
            if provider == "gemini":
                health["gemini"] = self.gemini_available
            elif provider == "mistral":
                health["mistral"] = self.mistral_available
        return health

    def _log_error(self, provider, error, prompt):
        logging.error(f"Provider {provider} failed for prompt '{prompt}': {error}")
        if self.user_context:
            logging.error(f"User/session context: {self.user_context}")

    def generate_ai_response(
        self,
        prompt,
        providers=None,
        return_mode=None,
        stream=False,
        confidence=False,
        **kwargs,
    ):
        self._check_rate_limit()
        """
        Generate response using selected AI providers with advanced features.
        providers: list or None - override which providers to use
        return_mode: str or None - 'aggregate', 'compare', or 'dict'
        stream: bool - if True, yield responses as they arrive (generator)
        confidence: bool - if True, estimate and return confidence scores
        """
        if providers is None:
            providers = [
                p
                for p in self.provider_priority
                if (
                    (p == "gemini" and self.use_gemini and self.gemini_available)
                    or (p == "mistral" and self.use_mistral and self.mistral_available)
                )
            ]
        if not providers:
            return "No AI provider response available."

        if return_mode is None:
            return_mode = self.return_mode

        if self.cache_enabled:
            cache_results = {}
            for provider in providers or []:
                key = self._cache_key(provider, prompt)
                if key in self._cache:
                    cache_results[provider] = self._cache[key]
            if cache_results and (
                not providers or len(cache_results) == len(providers)
            ):
                if return_mode == "dict":
                    return {"responses": cache_results}
                return "\n".join(
                    [
                        f"[{prov.upper()}]: {cache_results[prov]}"
                        for prov in cache_results
                    ]
                )

        responses = {}
        times = {}
        confidences = {}
        for provider in providers:
            last_exc = None
            for attempt in range(self.max_retries):
                start = time.time()
                try:
                    if provider == "gemini" and self.gemini_available:
                        settings = self.provider_settings.get("gemini", {})
                        prompt_to_use = self.format_prompt(prompt, **kwargs)
                        gemini_response = self.gemini_model.generate_content(
                            prompt_to_use, **settings
                        )
                        responses["gemini"] = gemini_response.text
                        confidences["gemini"] = (
                            getattr(gemini_response, "safety_ratings", None) or 0.9
                        )
                        if self.cache_enabled:
                            self._cache[self._cache_key("gemini", prompt)] = (
                                gemini_response.text
                            )
                        self._update_usage_stats("gemini", success=True)
                        # On first success, return immediately (failover)
                        if not stream:
                            responses = {"gemini": responses["gemini"]}
                            times = {"gemini": times["gemini"]}
                            confidences = {"gemini": confidences["gemini"]}
                        break
                    elif provider == "mistral" and self.mistral_available:
                        settings = self.provider_settings.get("mistral", {})
                        prompt_to_use = self.format_prompt(prompt, **kwargs)
                        mistral_response = self.mistral_client.chat.complete(
                            model=settings.get("model", self.mistral_model_name),
                            messages=[{"role": "user", "content": prompt_to_use}],
                            **{k: v for k, v in settings.items() if k != "model"},
                        )
                        responses["mistral"] = mistral_response.choices[
                            0
                        ].message.content
                        confidences["mistral"] = 0.9
                        if self.cache_enabled:
                            self._cache[self._cache_key("mistral", prompt)] = (
                                mistral_response.choices[0].message.content
                            )
                        self._update_usage_stats("mistral", success=True)
                        break
                except Exception as e:
                    last_exc = e
                    if self.verbose:
                        logging.warning(
                            f"Attempt {attempt + 1} failed for {provider}: {e}"
                        )
                    self._update_usage_stats(provider, success=False)
                    self._log_error(provider, e, prompt)
                    if attempt < self.max_retries - 1:
                        time.sleep(1**attempt)  # backoff
                    if self.verbose:
                        logging.warning(f"Retrying {provider} in {1**attempt}s...")
                    continue

                if self.verbose and last_exc:
                    logging.warning(
                        f"{provider} failed after {self.max_retries} attempts: {last_exc}"
                    )

            times[provider] = round(time.time() - start, 3)

        # If no responses, use fallback
        if not responses:
            return self.get_fallback_response(prompt)

        # Handle return modes
        if len(responses) == 1:
            result = list(responses.values())[0]
            if self.postprocess_hook:
                result = self.postprocess_hook(result)
            return result
        else:
            result_dict = {"responses": responses, "times": times}
            if confidence:
                result_dict["confidences"] = confidences
            if self.postprocess_hook:
                result_dict = self.postprocess_hook(result_dict)
            if return_mode == "dict":
                return result_dict
            elif return_mode == "compare":
                return "\n---\n".join(
                    [f"[{p.upper()}]: {responses[p]}" for p in responses]
                )
            else:  # aggregate
                return "\n".join([f"[{p.upper()}]: {responses[p]}" for p in responses])

    async def async_generate_ai_response(
        self, prompt, providers=None, return_mode=None, confidence=False, **kwargs
    ):
        """
        Async version of generate_ai_response for concurrent provider calls.
        """
        if providers is None:
            providers = [
                p
                for p in self.provider_priority
                if (
                    (p == "gemini" and self.use_gemini and self.gemini_available)
                    or (p == "mistral" and self.use_mistral and self.mistral_available)
                )
            ]
        if not providers:
            return "No AI provider response available."

        responses = {}
        times = {}
        confidences = {}

        async def call_provider(provider):
            start = time.time()
            try:
                if provider == "gemini" and self.gemini_available:
                    settings = self.provider_settings.get("gemini", {})
                    gemini_response = self.gemini_model.generate_content(
                        self.format_prompt(prompt, **kwargs), **settings
                    )
                    responses["gemini"] = gemini_response.text
                    confidences["gemini"] = (
                        getattr(gemini_response, "safety_ratings", None) or 0.9
                    )
                elif provider == "mistral" and self.mistral_available:
                    settings = self.provider_settings.get("mistral", {})
                    mistral_response = self.mistral_client.chat.complete(
                        model=settings.get("model", self.mistral_model_name),
                        messages=[
                            {
                                "role": "user",
                                "content": self.format_prompt(prompt, **kwargs),
                            }
                        ],
                        **{k: v for k, v in settings.items() if k != "model"},
                    )
                    responses["mistral"] = mistral_response.choices[0].message.content
                    confidences["mistral"] = 0.9
            except Exception as e:
                responses[provider] = f"[Error]: {e}"
                confidences[provider] = 0.0
            times[provider] = round(time.time() - start, 3)

        await asyncio.gather(*(call_provider(p) for p in providers))
        result_dict = {"responses": responses, "times": times}
        if confidence:
            result_dict["confidences"] = confidences
        if self.postprocess_hook:
            result_dict = self.postprocess_hook(result_dict)
        if return_mode == "dict":
            return result_dict
        elif return_mode == "compare":
            compare_str = "\n---\n".join(
                [
                    f"[{prov.upper()}] ({times.get(prov, 'N/A')}s):\n{responses.get(prov, 'No response')}"
                    + (
                        f"\nConfidence: {confidences.get(prov, 'N/A')}"
                        if confidence
                        else ""
                    )
                    for prov in providers
                ]
            )
            return compare_str
        else:  # aggregate
            agg_str = "\n".join(
                [
                    f"[{prov.upper()}]: {responses.get(prov, 'No response')}"
                    + (
                        f"\nConfidence: {confidences.get(prov, 'N/A')}"
                        if confidence
                        else ""
                    )
                    for prov in providers
                ]
            )
            return agg_str

    def get_fallback_response(self, prompt):
        """Override this method in child classes for specific fallback responses"""
        return "Fallback response - API providers unavailable"

    def process(
        self, input_data: Dict[str, Any], context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process input data using multiple AI providers
        """
        try:
            # Extract prompt from input data
            if isinstance(input_data, str):
                prompt = input_data
            elif isinstance(input_data, dict):
                prompt = input_data.get("prompt", str(input_data))
            else:
                prompt = str(input_data)

            # Generate response using multi-AI
            response = self.generate_response(prompt)

            return {
                "response": response,
                "success": True,
                "providers_used": [
                    p for p in self.provider_priority if self._is_provider_available(p)
                ],
            }

        except Exception as e:
            self.logger.error(f"Process failed: {e}")
            return {
                "response": self.get_fallback_response(str(input_data)),
                "success": False,
                "error": str(e),
            }

    def get_specialized_prompt_template(self):
        """
        Get default prompt template for MultiAIAgent
        """
        from agents.advanced_agent_base import (
            PromptTemplate,
            ReasoningMode,
            PromptComplexity,
        )

        return PromptTemplate(
            system_prompt="You are a helpful AI assistant with access to multiple AI providers.",
            user_prompt="Please provide a comprehensive response to the following query:",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            complexity=PromptComplexity.ADVANCED,
            context_variables={},
            validation_rules=[],
            examples=[],
            constraints=[],
        )

    def _is_provider_available(self, provider: str) -> bool:
        """Check if a provider is available and configured"""
        if provider == "gemini":
            return self.gemini_available
        elif provider == "mistral":
            return self.mistral_available
        return False
