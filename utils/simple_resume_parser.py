"""
Simple Resume Parser
===================

Reliable resume parsing using regex patterns and NLP techniques.
No external AI dependencies - works offline and consistently.
"""

import re
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Configure logging
logger = logging.getLogger(__name__)

class SimpleResumeParser:
    """
    Simple, reliable resume parser using pattern matching and heuristics.
    """
    
    def __init__(self):
        self.skill_patterns = self._load_skill_patterns()
        self.education_patterns = self._load_education_patterns()
        self.experience_patterns = self._load_experience_patterns()
    
    def _load_skill_patterns(self) -> Dict[str, List[str]]:
        """Load comprehensive skill patterns organized by category."""
        return {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C', 'Go', 'Rust',
                'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell',
                'Bash', 'PowerShell', 'VBA', 'Objective-C', 'Dart', 'Elixir', 'Haskell'
            ],
            'web_technologies': [
                'React', 'Angular', 'Vue.js', 'Vue', 'Node.js', 'Express', 'Django', 'Flask',
                'Spring', 'Laravel', 'Rails', 'ASP.NET', 'HTML5', 'HTML', 'CSS3', 'CSS',
                'SCSS', 'SASS', 'Bootstrap', 'Tailwind', 'jQuery', 'AJAX', 'REST', 'GraphQL',
                'WebSocket', 'Progressive Web App', 'PWA', 'Single Page Application', 'SPA'
            ],
            'databases': [
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Oracle',
                'SQL Server', 'SQLite', 'Cassandra', 'DynamoDB', 'Neo4j', 'InfluxDB',
                'CouchDB', 'MariaDB', 'Firebase', 'Firestore', 'Supabase'
            ],
            'cloud_platforms': [
                'AWS', 'Azure', 'Google Cloud', 'GCP', 'Digital Ocean', 'Heroku', 'Vercel',
                'Netlify', 'Cloudflare', 'IBM Cloud', 'Oracle Cloud', 'Alibaba Cloud'
            ],
            'devops_tools': [
                'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'CircleCI',
                'Travis CI', 'Ansible', 'Terraform', 'Vagrant', 'Chef', 'Puppet', 'Helm',
                'Istio', 'Prometheus', 'Grafana', 'ELK Stack', 'Splunk', 'Nagios'
            ],
            'version_control': [
                'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN', 'Mercurial', 'Perforce'
            ],
            'data_science': [
                'Machine Learning', 'ML', 'Deep Learning', 'AI', 'Artificial Intelligence',
                'Data Science', 'Data Analysis', 'Statistics', 'NLP', 'Computer Vision',
                'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy',
                'Matplotlib', 'Seaborn', 'Plotly', 'Jupyter', 'Apache Spark', 'Hadoop',
                'Tableau', 'Power BI', 'R Studio', 'SPSS', 'SAS'
            ],
            'mobile_development': [
                'iOS', 'Android', 'React Native', 'Flutter', 'Xamarin', 'Ionic', 'Cordova',
                'Swift', 'Objective-C', 'Kotlin', 'Java Android'
            ],
            'testing': [
                'Unit Testing', 'Integration Testing', 'Test Automation', 'Selenium', 'Jest',
                'Mocha', 'Chai', 'Cypress', 'Playwright', 'TestNG', 'JUnit', 'PyTest',
                'Postman', 'Insomnia', 'Load Testing', 'Performance Testing'
            ],
            'soft_skills': [
                'Leadership', 'Communication', 'Team Work', 'Problem Solving', 'Critical Thinking',
                'Project Management', 'Agile', 'Scrum', 'Kanban', 'Time Management',
                'Analytical Skills', 'Creativity', 'Adaptability', 'Collaboration',
                'Mentoring', 'Public Speaking', 'Presentation Skills', 'Negotiation'
            ],
            'methodologies': [
                'Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'CI/CD', 'TDD', 'BDD',
                'Microservices', 'SOA', 'MVC', 'MVP', 'MVVM', 'Clean Architecture',
                'Domain Driven Design', 'DDD', 'Event Sourcing', 'CQRS'
            ]
        }
    
    def _load_education_patterns(self) -> List[str]:
        """Load education-related patterns."""
        return [
            r'(Bachelor|Master|PhD|Doctorate|B\.Tech|M\.Tech|B\.S\.|M\.S\.|MBA|B\.A\.|M\.A\.|B\.E\.|M\.E\.)[^.]*',
            r'(University|College|Institute|School)[^.]*',
            r'(Computer Science|Engineering|Mathematics|Physics|Chemistry|Biology|Business|Economics|Finance)',
            r'(Degree|Diploma|Certificate|Certification)[^.]*',
            r'(GPA|CGPA|Grade)[\s:]*[\d.]+',
            r'\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}\b',  # Year ranges
            r'\b(19|20)\d{2}\s*[-–]\s*Present\b'
        ]
    
    def _load_experience_patterns(self) -> List[str]:
        """Load experience-related patterns."""
        return [
            r'(Software Engineer|Developer|Programmer|Analyst|Manager|Lead|Senior|Junior|Principal|Architect)',
            r'(Company|Corporation|Inc\.|Ltd\.|LLC|Technologies|Systems|Solutions)',
            r'\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}\b',  # Year ranges
            r'\b(19|20)\d{2}\s*[-–]\s*Present\b',
            r'(\d+)\+?\s*years?\s*(of)?\s*experience',
            r'experience\s*[:]\s*(\d+)\+?\s*years?'
        ]
    
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume text and extract structured information.
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Dict containing parsed resume information
        """
        if not resume_text or len(resume_text.strip()) < 10:
            return self._get_empty_result("Resume text is too short or empty")
        
        try:
            # Clean and preprocess text
            cleaned_text = self._clean_text(resume_text)
            
            # Extract different sections
            result = {
                'name': self._extract_name(cleaned_text),
                'contact': self._extract_contact_info(cleaned_text),
                'skills': self._extract_skills(cleaned_text),
                'education': self._extract_education(cleaned_text),
                'experience': self._extract_experience(cleaned_text),
                'years_of_experience': self._extract_years_of_experience(cleaned_text),
                'certifications': self._extract_certifications(cleaned_text),
                'projects': self._extract_projects(cleaned_text),
                'languages': self._extract_languages(cleaned_text),
                'summary': self._extract_summary(cleaned_text),
                'parsing_status': 'success',
                'parsed_at': datetime.now().isoformat()
            }
            
            # Add computed fields
            result['total_skills'] = len(result['skills']['all_skills'])
            result['skill_categories'] = len([cat for cat, skills in result['skills'].items() 
                                            if cat != 'all_skills' and skills])
            result['experience_level'] = self._determine_experience_level(result['years_of_experience'])
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            return self._get_empty_result(f"Parsing error: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@.,-]', ' ', text)
        return text.strip()
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name from resume."""
        lines = text.split('\n')
        
        # Look for name in first few lines
        for line in lines[:5]:
            line = line.strip()
            # Skip empty lines, emails, phones
            if (len(line) > 2 and len(line) < 50 and 
                not '@' in line and 
                not re.search(r'\d{3,}', line) and
                not line.lower().startswith(('resume', 'cv', 'curriculum'))):
                
                # Check if it looks like a name (2-4 words, mostly letters)
                words = line.split()
                if (2 <= len(words) <= 4 and 
                    all(word.replace('.', '').isalpha() for word in words)):
                    return line
        
        # Fallback: look for "Name:" pattern
        name_match = re.search(r'Name\s*[:]\s*([A-Za-z\s.]+)', text, re.IGNORECASE)
        if name_match:
            return name_match.group(1).strip()
        
        return "Unknown"
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information."""
        contact = {}
        
        # Email
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            contact['email'] = email_match.group()
        
        # Phone
        phone_patterns = [
            r'\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',
            r'\+?(\d{1,3})[-.\s]?(\d{3,4})[-.\s]?(\d{3,4})[-.\s]?(\d{3,4})'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact['phone'] = phone_match.group()
                break
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        # Location
        location_patterns = [
            r'Location\s*[:]\s*([^,\n]+(?:,\s*[^,\n]+)*)',
            r'Address\s*[:]\s*([^,\n]+(?:,\s*[^,\n]+)*)',
            r'([A-Za-z\s]+,\s*[A-Z]{2}(?:\s+\d{5})?)',  # City, State ZIP
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, text, re.IGNORECASE)
            if location_match:
                contact['location'] = location_match.group(1).strip()
                break
        
        return contact
    
    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills organized by category."""
        skills_result = {category: [] for category in self.skill_patterns.keys()}
        skills_result['all_skills'] = []
        
        text_lower = text.lower()
        
        for category, skills_list in self.skill_patterns.items():
            for skill in skills_list:
                # Create pattern that matches whole words
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    skills_result[category].append(skill)
                    if skill not in skills_result['all_skills']:
                        skills_result['all_skills'].append(skill)
        
        return skills_result
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information."""
        education = []
        
        for pattern in self.education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                if len(match.strip()) > 3:
                    education.append({
                        'description': match.strip(),
                        'type': self._classify_education(match)
                    })
        
        # Remove duplicates
        seen = set()
        unique_education = []
        for edu in education:
            if edu['description'] not in seen:
                seen.add(edu['description'])
                unique_education.append(edu)
        
        return unique_education[:5]  # Limit to 5 entries
    
    def _classify_education(self, education_text: str) -> str:
        """Classify education type."""
        text_lower = education_text.lower()
        
        if any(word in text_lower for word in ['phd', 'doctorate', 'doctoral']):
            return 'Doctorate'
        elif any(word in text_lower for word in ['master', 'm.s', 'm.tech', 'mba', 'm.a']):
            return 'Masters'
        elif any(word in text_lower for word in ['bachelor', 'b.s', 'b.tech', 'b.a', 'b.e']):
            return 'Bachelors'
        elif any(word in text_lower for word in ['diploma', 'certificate']):
            return 'Certificate'
        else:
            return 'Other'
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience."""
        experience = []
        
        # Look for job titles and companies
        job_patterns = [
            r'(Software Engineer|Developer|Programmer|Analyst|Manager|Lead|Senior|Junior|Principal|Architect)[^.]*',
            r'(Engineer|Developer|Analyst|Manager|Specialist|Consultant|Director|VP|CEO|CTO)[^.]*'
        ]
        
        for pattern in job_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 5:
                    experience.append({
                        'title': match.strip(),
                        'type': 'job_title'
                    })
        
        # Look for company names
        company_patterns = [
            r'(Company|Corporation|Inc\.|Ltd\.|LLC|Technologies|Systems|Solutions)[^.]*',
            r'at\s+([A-Z][a-zA-Z\s&]+(?:Inc\.|Ltd\.|LLC|Corp\.|Company)?)'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                if len(match.strip()) > 3:
                    experience.append({
                        'company': match.strip(),
                        'type': 'company'
                    })
        
        return experience[:10]  # Limit to 10 entries
    
    def _extract_years_of_experience(self, text: str) -> int:
        """Extract years of experience."""
        # Look for explicit years of experience
        years_patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'experience\s*[:]\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*year\s*experienced?'
        ]
        
        for pattern in years_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Estimate from experience level keywords
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect', 'director']):
            return 7
        elif any(word in text_lower for word in ['mid', 'intermediate', 'experienced']):
            return 4
        elif any(word in text_lower for word in ['junior', 'entry', 'fresher', 'graduate']):
            return 1
        else:
            # Count job positions as rough estimate
            job_count = len(re.findall(r'(engineer|developer|analyst|manager)', text_lower))
            return min(job_count * 2, 10)  # Assume 2 years per job, max 10
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications."""
        cert_patterns = [
            r'(AWS|Azure|Google Cloud|GCP)\s+(Certified|Professional|Associate)[^.]*',
            r'(Certified|Professional|Associate)\s+[A-Z][^.]*',
            r'(Scrum Master|PMP|CISSP|CISA|CISM)[^.]*',
            r'Certification\s*[:]\s*([^.\n]+)'
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                if len(match.strip()) > 3:
                    certifications.append(match.strip())
        
        return list(set(certifications))[:5]  # Remove duplicates, limit to 5
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract project information."""
        project_patterns = [
            r'Project\s*[:]\s*([^.\n]+)',
            r'Projects?\s*[:]\s*([^.\n]+)',
            r'Built\s+([^.\n]+)',
            r'Developed\s+([^.\n]+)',
            r'Created\s+([^.\n]+)'
        ]
        
        projects = []
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 10:
                    projects.append(match.strip())
        
        return list(set(projects))[:5]  # Remove duplicates, limit to 5
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract spoken languages."""
        language_patterns = [
            r'Languages?\s*[:]\s*([^.\n]+)',
            r'(English|Spanish|French|German|Chinese|Japanese|Korean|Hindi|Arabic|Portuguese|Russian|Italian)\s*\([^)]+\)',
            r'(Native|Fluent|Conversational|Basic)\s+(English|Spanish|French|German|Chinese|Japanese|Korean|Hindi|Arabic|Portuguese|Russian|Italian)'
        ]
        
        languages = []
        for pattern in language_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                if len(match.strip()) > 2:
                    languages.append(match.strip())
        
        return list(set(languages))[:5]  # Remove duplicates, limit to 5
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary."""
        summary_patterns = [
            r'Summary\s*[:]\s*([^.\n]+(?:\.[^.\n]+)*)',
            r'Professional Summary\s*[:]\s*([^.\n]+(?:\.[^.\n]+)*)',
            r'Objective\s*[:]\s*([^.\n]+(?:\.[^.\n]+)*)',
            r'Profile\s*[:]\s*([^.\n]+(?:\.[^.\n]+)*)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                summary = match.group(1).strip()
                if len(summary) > 20:
                    return summary[:500]  # Limit to 500 characters
        
        # Fallback: use first paragraph if it looks like a summary
        paragraphs = text.split('\n\n')
        for para in paragraphs[:3]:
            para = para.strip()
            if (len(para) > 50 and 
                any(word in para.lower() for word in ['experience', 'skilled', 'professional', 'expertise'])):
                return para[:500]
        
        return ""
    
    def _determine_experience_level(self, years: int) -> str:
        """Determine experience level based on years."""
        if years == 0:
            return "Entry Level"
        elif years <= 2:
            return "Junior"
        elif years <= 5:
            return "Mid Level"
        elif years <= 10:
            return "Senior"
        else:
            return "Expert"
    
    def _get_empty_result(self, error_message: str) -> Dict[str, Any]:
        """Return empty result structure with error."""
        return {
            'name': 'Unknown',
            'contact': {},
            'skills': {category: [] for category in self.skill_patterns.keys()},
            'education': [],
            'experience': [],
            'years_of_experience': 0,
            'certifications': [],
            'projects': [],
            'languages': [],
            'summary': '',
            'total_skills': 0,
            'skill_categories': 0,
            'experience_level': 'Unknown',
            'parsing_status': 'error',
            'error': error_message,
            'parsed_at': datetime.now().isoformat()
        }

# Convenience function for easy import
def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Parse resume text and return structured data.
    
    Args:
        resume_text: Raw resume text
        
    Returns:
        Dict containing parsed resume information
    """
    parser = SimpleResumeParser()
    return parser.parse_resume(resume_text)