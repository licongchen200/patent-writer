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
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    
    print(f"\n✓ Enhanced patent exported to: {filepath}")
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
        claim language and structure.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 3: Technical Detail Enhancer
    technical_enhancer = Agent(
        role='Technical Detail Enhancement Specialist',
        goal='Identify areas where technical descriptions could be more detailed or clearer',
        backstory="""Technical writer and patent specialist who reviews technical descriptions
        for completeness, clarity, and enablement requirements. Suggests additional technical
        details, embodiments, and clarifications.""",
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
    
    # Agent 5: Quality Reviewer
    quality_reviewer = Agent(
        role='Patent Quality Assurance Reviewer',
        goal='Comprehensive review of the entire application for quality and completeness',
        backstory="""Senior patent professional who performs final quality checks on patent applications.
        Reviews for completeness, consistency, USPTO compliance, and overall quality.""",
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
    
    # Task 3: Technical Detail Enhancement
    task3 = Task(
        description=f"""Review technical descriptions and suggest enhancements:
        
        Review the detailed description and technical sections for:
        1. Areas lacking sufficient technical detail
        2. Concepts that could be explained more clearly
        3. Additional embodiments or variations to describe
        4. Potential enablement issues
        5. Missing technical specifications or parameters
        
        Provide specific enhancement recommendations for technical sections.""",
        agent=technical_enhancer,
        expected_output="Technical description enhancement recommendations with specific additions"
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
    
    # Task 5: Final Quality Review
    task5 = Task(
        description=f"""Perform comprehensive quality review and create final recommendations:
        
        Review all enhancement suggestions from other agents and:
        1. Assess overall application quality
        2. Identify most critical enhancements to implement
        3. Ensure consistency across all sections
        4. Check USPTO formal requirements compliance
        5. Create prioritized enhancement action plan
        
        Provide final quality assessment and prioritized enhancement recommendations.""",
        agent=quality_reviewer,
        expected_output="Comprehensive quality review and prioritized enhancement action plan"
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
    structured_data = {
        'title': 'ENHANCED: ' + (existing_patent.split('\n')[2] if len(existing_patent.split('\n')) > 2 else 'PATENT APPLICATION'),
        'abstract': existing_patent.split('ABSTRACT')[1].split('\n\n')[0] if 'ABSTRACT' in existing_patent else '',
        'field': existing_patent.split('FIELD OF THE INVENTION')[1].split('\n\n')[0] if 'FIELD OF THE INVENTION' in existing_patent else '',
        'background': existing_patent.split('BACKGROUND')[1].split('SUMMARY')[0] if 'BACKGROUND' in existing_patent else '',
        'prior_art': str(tasks[0].output) if len(tasks) > 0 and hasattr(tasks[0], 'output') else '',
        'summary': existing_patent.split('SUMMARY')[1].split('CLAIMS')[0] if 'SUMMARY' in existing_patent else '',
        'detailed_description': existing_patent.split('DETAILED DESCRIPTION')[1].split('ADVANTAGES')[0] if 'DETAILED DESCRIPTION' in existing_patent else '',
        'claims': existing_patent.split('CLAIMS')[1].split('DETAILED')[0] if 'CLAIMS' in existing_patent else '',
        'enhancements': str(result)
    }
    
    # Export results
    md_file = export_to_markdown(structured_data, "patent_enhanced.md")
    export_to_json(result, "patent_enhanced.json")
    
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\n✓ Enhanced patent application exported to:")
    print(f"  - {md_file}")
    print(f"  - output/patent_enhanced.json")
    print(f"\nReview the output files to see AI-generated enhancement recommendations.")
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
