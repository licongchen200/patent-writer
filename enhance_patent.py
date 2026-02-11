#!/usr/bin/env python3
"""
Patent Enhancement System
Reads existing patent applications and enhances them using AI agents.
"""
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from datetime import datetime
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure OPENAI_API_KEY is set (required by CrewAI even for custom base URLs)
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "dummy-key-not-needed")

# ============================================================================
# CUSTOM TOOLS FOR PATENT SEARCH
# ============================================================================

@tool("USPTO Search Tool")
def uspto_search(query: str) -> str:
    """Search USPTO patent database for relevant patents."""
    search_tool = SerperDevTool()
    results = search_tool.run(f"site:uspto.gov OR site:patents.google.com {query}")
    return f"USPTO Search Results for '{query}':\n{results}"

@tool("Google Patents Search Tool")
def google_patents_search(query: str) -> str:
    """Search Google Patents for prior art and related patents."""
    search_tool = SerperDevTool()
    results = search_tool.run(f"site:patents.google.com {query}")
    return f"Google Patents Search Results:\n{results}"

# Standard tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_to_markdown(patent_data: dict, filename: str = "patent_enhanced.md"):
    """Export enhanced patent to markdown."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    md_content = []
    
    # Title
    title = patent_data.get('title', 'ENHANCED PATENT APPLICATION')
    md_content.append(f"# {title}")
    md_content.append("")
    
    # Metadata
    md_content.append("---")
    md_content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_content.append("**Type:** Enhanced Patent Application")
    if patent_data.get('confidence_score'):
        md_content.append(f"**Confidence Score:** {patent_data.get('confidence_score')}/100")
        md_content.append(f"**Patentability Assessment:** {patent_data.get('confidence_assessment', 'N/A')}")
    md_content.append("---")
    md_content.append("")
    
    # Table of Contents
    md_content.append("## Table of Contents")
    md_content.append("")
    md_content.append("1. [Abstract](#abstract)")
    md_content.append("2. [Field of the Invention](#field-of-the-invention)")
    md_content.append("3. [Background of the Invention](#background-of-the-invention)")
    md_content.append("4. [Prior Art Analysis](#prior-art-analysis)")
    md_content.append("5. [Summary of the Invention](#summary-of-the-invention)")
    md_content.append("6. [Detailed Description](#detailed-description)")
    md_content.append("7. [Claims](#claims)")
    md_content.append("8. [Enhancement Recommendations](#enhancement-recommendations)")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Abstract
    md_content.append("## Abstract")
    md_content.append("")
    md_content.append(patent_data.get('abstract', ''))
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Field of Invention
    md_content.append("## Field of the Invention")
    md_content.append("")
    md_content.append(patent_data.get('field', ''))
    md_content.append("")
    
    # Background
    md_content.append("## Background of the Invention")
    md_content.append("")
    md_content.append(patent_data.get('background', ''))
    md_content.append("")
    
    # Prior Art
    md_content.append("## Prior Art Analysis")
    md_content.append("")
    md_content.append(patent_data.get('prior_art', ''))
    md_content.append("")
    
    # Summary
    md_content.append("## Summary of the Invention")
    md_content.append("")
    md_content.append(patent_data.get('summary', ''))
    md_content.append("")
    
    # Detailed Description
    md_content.append("## Detailed Description")
    md_content.append("")
    md_content.append(patent_data.get('detailed_description', ''))
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Claims
    md_content.append("## Claims")
    md_content.append("")
    md_content.append(patent_data.get('claims', ''))
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Enhancement Recommendations
    if patent_data.get('enhancements'):
        md_content.append("## Enhancement Recommendations")
        md_content.append("")
        md_content.append(patent_data.get('enhancements', ''))
        md_content.append("")
    
    # System Architecture Diagrams
    if patent_data.get('diagrams'):
        md_content.append("## System Architecture & Diagrams")
        md_content.append("")
        md_content.append(patent_data.get('diagrams', ''))
        md_content.append("")
    
    # Confidence Analysis
    if patent_data.get('confidence_analysis'):
        md_content.append("## Patent Confidence Analysis")
        md_content.append("")
        md_content.append(patent_data.get('confidence_analysis', ''))
        md_content.append("")
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    
    print(f"\n✓ Enhanced patent exported to: {filepath}")
    return filepath

def export_to_html(patent_data: dict, filename: str = "patent_enhanced.html"):
    """Export enhanced patent to HTML with Mermaid diagram support."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    title = patent_data.get('title', 'ENHANCED PATENT APPLICATION')
    confidence_score = patent_data.get('confidence_score', 'N/A')
    confidence_assessment = patent_data.get('confidence_assessment', 'N/A')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.8;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 60px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            text-align: center;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #0066cc;
            margin-top: 40px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #333;
            margin-top: 30px;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #0066cc;
            margin: 30px 0;
        }}
        .confidence-badge {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .confidence-high {{ background: #d4edda; color: #155724; }}
        .confidence-medium {{ background: #fff3cd; color: #856404; }}
        .confidence-low {{ background: #f8d7da; color: #721c24; }}
        .section {{
            margin: 40px 0;
            padding: 20px;
            background: #fafafa;
            border-radius: 5px;
        }}
        .mermaid {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .toc {{
            background: #f0f7ff;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
        }}
        .toc a {{
            color: #0066cc;
            text-decoration: none;
            display: block;
            padding: 5px 0;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
    </style>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="metadata">
            <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>Type:</strong> Enhanced Patent Application<br>
            <strong>Confidence Score:</strong> <span class="confidence-badge confidence-{'high' if isinstance(confidence_score, (int, float)) and confidence_score >= 75 else 'medium' if isinstance(confidence_score, (int, float)) and confidence_score >= 50 else 'low'}">{confidence_score}/100</span><br>
            <strong>Patentability Assessment:</strong> {confidence_assessment}
        </div>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <a href="#abstract">1. Abstract</a>
            <a href="#field">2. Field of the Invention</a>
            <a href="#background">3. Background of the Invention</a>
            <a href="#prior-art">4. Prior Art Analysis</a>
            <a href="#summary">5. Summary of the Invention</a>
            <a href="#detailed">6. Detailed Description</a>
            <a href="#claims">7. Claims</a>
            <a href="#diagrams">8. System Architecture & Diagrams</a>
            <a href="#enhancements">9. Enhancement Recommendations</a>
            <a href="#confidence">10. Patent Confidence Analysis</a>
        </div>
        
        <div id="abstract" class="section">
            <h2>Abstract</h2>
            <p>{patent_data.get('abstract', '').replace(chr(10), '<br>')}</p>
        </div>
        
        <div id="field" class="section">
            <h2>Field of the Invention</h2>
            <p>{patent_data.get('field', '').replace(chr(10), '<br>')}</p>
        </div>
        
        <div id="background" class="section">
            <h2>Background of the Invention</h2>
            <div>{patent_data.get('background', '').replace(chr(10), '<br>')}</div>
        </div>
        
        <div id="prior-art" class="section">
            <h2>Prior Art Analysis</h2>
            <div>{patent_data.get('prior_art', '').replace(chr(10), '<br>')}</div>
        </div>
        
        <div id="summary" class="section">
            <h2>Summary of the Invention</h2>
            <div>{patent_data.get('summary', '').replace(chr(10), '<br>')}</div>
        </div>
        
        <div id="detailed" class="section">
            <h2>Detailed Description</h2>
            <div>{patent_data.get('detailed_description', '').replace(chr(10), '<br>')}</div>
        </div>
        
        <div id="claims" class="section">
            <h2>Claims</h2>
            <pre>{patent_data.get('claims', '')}</pre>
        </div>
        
        <div id="diagrams" class="section">
            <h2>System Architecture & Diagrams</h2>
            <div>{patent_data.get('diagrams', '').replace('```mermaid', '<div class="mermaid">').replace('```', '</div>')}</div>
        </div>
        
        <div id="enhancements" class="section">
            <h2>Enhancement Recommendations</h2>
            <div>{patent_data.get('enhancements', '').replace(chr(10), '<br>')}</div>
        </div>
        
        <div id="confidence" class="section">
            <h2>Patent Confidence Analysis</h2>
            <div>{patent_data.get('confidence_analysis', '').replace(chr(10), '<br>')}</div>
        </div>
    </div>
</body>
</html>
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Enhanced patent HTML exported to: {filepath}")
    return filepath

def export_to_json(result, filename: str = "patent_enhanced.json"):
    """Save enhancement results to JSON."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    patent_data = {
        'timestamp': datetime.now().isoformat(),
        'raw_output': str(result),
        'sections': {}
    }
    
    with open(filepath, 'w') as f:
        json.dump(patent_data, f, indent=2)
    
    print(f"\n✓ Enhancement data saved to: {filepath}")
    return patent_data

# ============================================================================
# PATENT ENHANCEMENT AGENTS
# ============================================================================

def create_enhancement_agents(existing_patent_text: str):
    """Create specialized agents for patent enhancement."""
    
    # Agent 1: Prior Art Enhancer
    prior_art_agent = Agent(
        role='Patent Prior Art Specialist',
        goal='Review existing prior art section and identify gaps or additional relevant patents',
        backstory="""Expert in patent search with access to USPTO and Google Patents databases.
        Specializes in finding additional relevant prior art and strengthening prior art analysis.""",
        tools=[uspto_search, google_patents_search, search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 2: Claims Strengthening Expert
    claims_expert = Agent(
        role='Patent Claims Strengthening Expert',
        goal='Analyze existing claims and suggest improvements for broader or stronger protection',
        backstory="""Senior patent attorney specializing in claim drafting. Reviews existing claims
        for potential weaknesses, suggests dependent claims to expand protection, and ensures proper
        claim language and structure. Also creates Mermaid diagrams to visualize claim relationships.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 3: Technical Detail Enhancer
    technical_enhancer = Agent(
        role='Technical Detail Enhancement Specialist',
        goal='Identify areas where technical descriptions could be more detailed or clearer, and create system architecture diagrams',
        backstory="""Technical writer and patent specialist who reviews technical descriptions
        for completeness, clarity, and enablement requirements. Expert at creating Mermaid diagrams
        including flowcharts, sequence diagrams, and system architecture diagrams to visualize the invention.
        Suggests additional technical details, embodiments, and clarifications.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 4: Novelty Validator
    novelty_validator = Agent(
        role='Patent Novelty Validator',
        goal='Assess the novelty and non-obviousness of the invention compared to prior art',
        backstory="""Patent examiner with expertise in evaluating patentability. Reviews the invention
        against prior art to identify unique aspects and suggest ways to emphasize novelty.""",
        tools=[uspto_search, google_patents_search, search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 5: Quality Reviewer & Confidence Scorer
    quality_reviewer = Agent(
        role='Patent Quality Assurance Reviewer & Confidence Scorer',
        goal='Comprehensive review of the entire application for quality, completeness, and provide patentability confidence score',
        backstory="""Senior patent professional who performs final quality checks on patent applications.
        Reviews for completeness, consistency, USPTO compliance, and overall quality. Expert at assessing
        patent strength and providing confidence scores (0-100) based on novelty, prior art differentiation,
        claim strength, technical enablement, and commercial viability.""",
        tools=[],
        verbose=True,
        allow_delegation=False
    )
    
    return [prior_art_agent, claims_expert, technical_enhancer, novelty_validator, quality_reviewer]

def create_enhancement_tasks(agents, existing_patent_text: str):
    """Create tasks for patent enhancement."""
    
    prior_art_agent, claims_expert, technical_enhancer, novelty_validator, quality_reviewer = agents
    
    # Task 1: Enhanced Prior Art Search
    task1 = Task(
        description=f"""Review the existing patent application and enhance the prior art analysis:
        
        EXISTING PATENT:
        {existing_patent_text[:2000]}...
        
        Your task:
        1. Review the existing prior art section
        2. Search for additional relevant patents not mentioned
        3. Identify any gaps in the prior art analysis
        4. Suggest additional patent references with numbers and descriptions
        5. Recommend how to better distinguish the invention from prior art
        
        Provide a comprehensive report on prior art enhancements.""",
        agent=prior_art_agent,
        expected_output="Detailed prior art enhancement report with specific patent numbers and recommendations"
    )
    
    # Task 2: Claims Enhancement
    task2 = Task(
        description=f"""Review the existing claims and suggest improvements:
        
        EXISTING PATENT (Claims Section):
        {existing_patent_text[existing_patent_text.find('CLAIMS'):existing_patent_text.find('CLAIMS')+3000] if 'CLAIMS' in existing_patent_text else 'No claims section found'}
        
        Your task:
        1. Analyze existing independent and dependent claims
        2. Identify potential weaknesses or ambiguities
        3. Suggest additional dependent claims for broader protection
        4. Recommend rewording for clarity and strength
        5. Ensure claims properly capture the invention's novelty
        
        Provide specific claim enhancement recommendations.""",
        agent=claims_expert,
        expected_output="Detailed claims enhancement recommendations with specific rewording suggestions"
    )
    
    # Task 3: Technical Detail Enhancement with Diagrams
    task3 = Task(
        description=f"""Review technical descriptions, suggest enhancements, and CREATE MERMAID DIAGRAMS:
        
        Review the detailed description and technical sections for:
        1. Areas lacking sufficient technical detail
        2. Concepts that could be explained more clearly
        3. Additional embodiments or variations to describe
        4. Potential enablement issues
        5. Missing technical specifications or parameters
        
        IMPORTANT: CREATE MERMAID DIAGRAMS including:
        - System Architecture Diagram (flowchart showing main components)
        - Sequence Diagram (showing interaction flow between components)
        - State Diagram (if applicable, showing system states)
        - Component Interaction Diagram
        
        Use proper Mermaid syntax wrapped in ```mermaid code blocks.
        Example:
        ```mermaid
        flowchart TD
            A[Client Browser] --> B[Object Storage]
            B --> C[Error Status File]
            D[Backend Logger] --> B
        ```
        
        Provide specific enhancement recommendations with at least 2-3 Mermaid diagrams.""",
        agent=technical_enhancer,
        expected_output="Technical description enhancements with 2-3 Mermaid diagrams in proper markdown code blocks"
    )
    
    # Task 4: Novelty Assessment
    task4 = Task(
        description=f"""Assess the invention's novelty and provide recommendations:
        
        Based on the patent application and prior art:
        1. Identify the most novel aspects of the invention
        2. Suggest how to better emphasize unique features
        3. Assess potential obviousness challenges
        4. Recommend defensive strategies against prior art
        5. Suggest language to strengthen novelty arguments
        
        Provide a novelty assessment and enhancement strategy.""",
        agent=novelty_validator,
        expected_output="Novelty assessment report with specific enhancement strategies"
    )
    
    # Task 5: Final Quality Review with Confidence Score
    task5 = Task(
        description=f"""Perform comprehensive quality review, provide confidence score, and create final recommendations:
        
        Review all enhancement suggestions from other agents and:
        1. Assess overall application quality
        2. Identify most critical enhancements to implement
        3. Ensure consistency across all sections
        4. Check USPTO formal requirements compliance
        5. Create prioritized enhancement action plan
        
        CRITICAL: Provide a PATENT CONFIDENCE SCORE (0-100) based on:
        - Novelty Assessment (0-25 points): How unique is the invention?
        - Prior Art Differentiation (0-20 points): How well distinguished from existing patents?
        - Claim Strength (0-20 points): How defensible are the claims?
        - Technical Enablement (0-20 points): Is the invention fully described and reproducible?
        - Commercial Viability (0-15 points): Market potential and practical implementation
        
        Score Interpretation:
        - 85-100: Excellent - Strong patent with high likelihood of approval
        - 70-84: Good - Solid patent with minor improvements needed
        - 50-69: Fair - Moderate strength, significant enhancements recommended
        - Below 50: Weak - Major concerns, substantial revision required
        
        OUTPUT FORMAT:
        ## Patent Confidence Score: [X]/100
        ## Assessment: [Excellent/Good/Fair/Weak]
        
        ### Score Breakdown:
        - Novelty: [X]/25 - [reasoning]
        - Prior Art Differentiation: [X]/20 - [reasoning]
        - Claim Strength: [X]/20 - [reasoning]
        - Technical Enablement: [X]/20 - [reasoning]
        - Commercial Viability: [X]/15 - [reasoning]
        
        ### Key Strengths:
        [List 3-5 major strengths]
        
        ### Key Weaknesses:
        [List 3-5 areas of concern]
        
        ### Recommended Actions:
        [Prioritized list of improvements]
        
        Provide final quality assessment with detailed confidence analysis.""",
        agent=quality_reviewer,
        expected_output="Comprehensive quality review with detailed confidence score (0-100), score breakdown, and prioritized enhancement action plan"
    )
    
    return [task1, task2, task3, task4, task5]

# ============================================================================
# MAIN ENHANCEMENT FUNCTION
# ============================================================================

def enhance_patent(input_file: str):
    """Main function to enhance an existing patent application."""
    
    print("=" * 80)
    print("PATENT ENHANCEMENT SYSTEM")
    print("=" * 80)
    print(f"\nReading patent from: {input_file}")
    
    # Read existing patent
    try:
        with open(input_file, 'r',encoding='utf-8') as f:
            existing_patent = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    print(f"✓ Patent loaded ({len(existing_patent)} characters)")
    print(f"\nStarting AI-powered enhancement process...")
    print("This will take several minutes as agents analyze the patent.\n")
    
    # Create agents and tasks
    agents = create_enhancement_agents(existing_patent)
    tasks = create_enhancement_tasks(agents, existing_patent)
    
    # Create and run crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    print("\n" + "=" * 80)
    print("STARTING ENHANCEMENT ANALYSIS")
    print("=" * 80 + "\n")
    
    result = crew.kickoff()
    
    print("\n" + "=" * 80)
    print("ENHANCEMENT COMPLETE")
    print("=" * 80 + "\n")
    
    # Parse and structure the results
    result_str = str(result)
    
    # Extract confidence score from quality review
    confidence_score = 'N/A'
    confidence_assessment = 'Pending Analysis'
    if 'Patent Confidence Score:' in result_str or 'Confidence Score:' in result_str:
        import re
        score_match = re.search(r'(?:Patent )?Confidence Score:?\s*(\d+)/100', result_str)
        if score_match:
            confidence_score = int(score_match.group(1))
            if confidence_score >= 85:
                confidence_assessment = 'Excellent - Strong patent with high likelihood of approval'
            elif confidence_score >= 70:
                confidence_assessment = 'Good - Solid patent with minor improvements needed'
            elif confidence_score >= 50:
                confidence_assessment = 'Fair - Moderate strength, significant enhancements recommended'
            else:
                confidence_assessment = 'Weak - Major concerns, substantial revision required'
    
    # Extract diagrams from technical enhancement task
    diagrams = ''
    if len(tasks) > 2 and hasattr(tasks[2], 'output'):
        task3_output = str(tasks[2].output)
        if '```mermaid' in task3_output:
            diagrams = task3_output
    
    # Extract confidence analysis from quality review
    confidence_analysis = ''
    if len(tasks) > 4 and hasattr(tasks[4], 'output'):
        confidence_analysis = str(tasks[4].output)
    
    structured_data = {
        'title': 'ENHANCED: ' + (existing_patent.split('\n')[2] if len(existing_patent.split('\n')) > 2 else 'PATENT APPLICATION'),
        'abstract': existing_patent.split('ABSTRACT')[1].split('\n\n')[0] if 'ABSTRACT' in existing_patent else '',
        'field': existing_patent.split('FIELD OF THE INVENTION')[1].split('\n\n')[0] if 'FIELD OF THE INVENTION' in existing_patent else '',
        'background': existing_patent.split('BACKGROUND')[1].split('SUMMARY')[0] if 'BACKGROUND' in existing_patent else '',
        'prior_art': str(tasks[0].output) if len(tasks) > 0 and hasattr(tasks[0], 'output') else '',
        'summary': existing_patent.split('SUMMARY')[1].split('CLAIMS')[0] if 'SUMMARY' in existing_patent else '',
        'detailed_description': existing_patent.split('DETAILED DESCRIPTION')[1].split('ADVANTAGES')[0] if 'DETAILED DESCRIPTION' in existing_patent else '',
        'claims': existing_patent.split('CLAIMS')[1].split('DETAILED')[0] if 'CLAIMS' in existing_patent else '',
        'enhancements': result_str,
        'diagrams': diagrams,
        'confidence_score': confidence_score,
        'confidence_assessment': confidence_assessment,
        'confidence_analysis': confidence_analysis
    }
    
    # Export results in both formats
    md_file = export_to_markdown(structured_data, "patent_enhanced.md")
    html_file = export_to_html(structured_data, "patent_enhanced.html")
    export_to_json(result, "patent_enhanced.json")
    
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\n✓ Enhanced patent application exported to:")
    print(f"  - {md_file}")
    print(f"  - {html_file}")
    print(f"  - output/patent_enhanced.json")
    if confidence_score != 'N/A':
        print(f"\n✓ Patent Confidence Score: {confidence_score}/100")
        print(f"  Assessment: {confidence_assessment}")
    print(f"\nReview the output files to see AI-generated enhancement recommendations.")
    print(f"Open the HTML file in your browser for best viewing experience with diagrams.")
    print("=" * 80 + "\n")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    input_file = "input/error-monitoring-patent.txt"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Usage: python enhance_patent.py [input_file]")
        print(f"Default: input/error-monitoring-patent.txt")
        sys.exit(1)
    
    enhance_patent(input_file)
