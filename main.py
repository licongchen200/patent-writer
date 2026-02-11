from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, BaseTool
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os
import json

# ============================================================================
# CUSTOM TOOLS FOR PATENT SEARCH
# ============================================================================

class USPTOSearchTool(BaseTool):
    name: str = "USPTO Search Tool"
    description: str = "Search USPTO patent database for relevant patents."
    
    def _run(self, query: str) -> str:
        """Search USPTO patent database."""
        search_tool = SerperDevTool()
        results = search_tool.run(f"site:uspto.gov OR site:patents.google.com {query}")
        return f"USPTO Search Results for '{query}':\n{results}"

class GooglePatentsSearchTool(BaseTool):
    name: str = "Google Patents Search Tool"
    description: str = "Search Google Patents for prior art and related patents."
    
    def _run(self, query: str) -> str:
        """Search Google Patents."""
        search_tool = SerperDevTool()
        results = search_tool.run(f"site:patents.google.com {query}")
        return f"Google Patents Search Results:\n{results}"

# Instantiate custom tools
uspto_search = USPTOSearchTool()
google_patents_search = GooglePatentsSearchTool()

# Standard tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# ============================================================================
# DOCUMENT EXPORT FUNCTION
# ============================================================================

def export_to_docx(patent_data: dict, filename: str = "patent_application.docx"):
    """Export patent application to a properly formatted .docx file.
    
    Args:
        patent_data: Dictionary containing all patent sections
        filename: Output filename
    """
    doc = Document()
    
    # Title
    title = doc.add_heading(patent_data.get('title', 'PATENT APPLICATION'), 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Metadata
    doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc.add_paragraph("=" * 80)
    doc.add_paragraph()
    
    # Abstract
    doc.add_heading('ABSTRACT', 1)
    doc.add_paragraph(patent_data.get('abstract', ''))
    doc.add_page_break()
    
    # Field of Invention
    doc.add_heading('FIELD OF THE INVENTION', 1)
    doc.add_paragraph(patent_data.get('field', ''))
    doc.add_paragraph()
    
    # Background
    doc.add_heading('BACKGROUND OF THE INVENTION', 1)
    doc.add_paragraph(patent_data.get('background', ''))
    doc.add_paragraph()
    
    # Prior Art
    doc.add_heading('PRIOR ART ANALYSIS', 1)
    doc.add_paragraph(patent_data.get('prior_art', ''))
    doc.add_paragraph()
    
    # Summary
    doc.add_heading('SUMMARY OF THE INVENTION', 1)
    doc.add_paragraph(patent_data.get('summary', ''))
    doc.add_paragraph()
    
    # Detailed Description
    doc.add_heading('DETAILED DESCRIPTION', 1)
    doc.add_paragraph(patent_data.get('detailed_description', ''))
    doc.add_page_break()
    
    # Claims
    doc.add_heading('CLAIMS', 1)
    claims_text = patent_data.get('claims', '')
    doc.add_paragraph(claims_text)
    doc.add_page_break()
    
    # Review Comments
    if patent_data.get('review_comments'):
        doc.add_heading('REVIEW COMMENTS AND RECOMMENDATIONS', 1)
        doc.add_paragraph(patent_data.get('review_comments', ''))
    
    # Save document
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    doc.save(filepath)
    print(f"\n✓ Patent application exported to: {filepath}")
    return filepath

def export_sections_to_json(result, filename: str = "patent_data.json"):
    """Save the crew output to JSON for processing."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Parse the result into structured data
    patent_data = {
        'timestamp': datetime.now().isoformat(),
        'raw_output': str(result),
        'sections': {}
    }
    
    with open(filepath, 'w') as f:
        json.dump(patent_data, f, indent=2)
    
    print(f"\n✓ Patent data saved to: {filepath}")
    return patent_data

# ============================================================================
# HUMAN-IN-THE-LOOP APPROVAL
# ============================================================================

def human_approval_check(patent_data: dict, iteration: int = 1) -> dict:
    """Request human approval before finalizing the patent application.
    
    Args:
        patent_data: The complete patent application data
        iteration: Current iteration number
        
    Returns:
        Dictionary with approval status and feedback
    """
    print("\n" + "=" * 80)
    print(f"HUMAN REVIEW REQUIRED (Iteration {iteration})")
    print("=" * 80)
    print("\nThe patent application draft is ready for your review.")
    print("\nPlease review the generated documents in the 'output' folder.")
    
    print("\nOptions:")
    print("  1. Approve and finalize")
    print("  2. Request revisions (will iterate with feedback)")
    print("  3. Save draft and exit")
    
    while True:
        choice = input("\nYour decision (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            if choice == '1':
                print("\n✓ Application approved!")
                return {'approved': True, 'feedback': None}
            elif choice == '2':
                print("\nWhat revisions are needed? Be specific:")
                feedback = input("Your feedback: ").strip()
                print("\n✓ Feedback recorded. Will re-run revision cycle...")
                return {'approved': False, 'feedback': feedback}
            else:
                print("\n✓ Draft saved. Exiting...")
                return {'approved': None, 'feedback': None}
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# ============================================================================
# AGENTS DEFINITION
# ============================================================================

# Agent 1: Prior Art Researcher
prior_art_researcher = Agent(
    role='Patent Prior Art Researcher',
    goal='Find all relevant existing patents and publications using USPTO and Google Patents',
    backstory='''Expert patent searcher with 15 years experience. 
    You know how to search USPTO, Google Patents, and academic databases.
    You identify similar inventions and their key differences.
    You always provide specific patent numbers and classification codes.''',
    tools=[uspto_search, google_patents_search, search_tool, scrape_tool],
    verbose=True
)

# Agent 2: Technical Analyzer
tech_analyzer = Agent(
    role='Technical Patent Analyst',
    goal='Analyze the technical aspects and innovations',
    backstory='''Senior engineer who understands technical details deeply.
    You break down inventions into components, methods, and systems.
    You identify the technical problem solved and the solution provided.''',
    verbose=True
)

# Agent 3: Novelty Assessor
novelty_assessor = Agent(
    role='Patent Novelty Assessor',
    goal='Determine what is truly novel and non-obvious',
    backstory='''Patent examiner with expertise in determining novelty.
    You compare the invention against prior art to identify unique aspects.
    You understand the "non-obvious" requirement for patentability.''',
    verbose=True
)

# Agent 4: Claims Writer
claims_writer = Agent(
    role='Patent Claims Drafter',
    goal='Draft strong, defensible patent claims',
    backstory='''Patent attorney specializing in claim drafting.
    You write independent and dependent claims that are broad yet specific.
    You use proper legal language and structure for USPTO requirements.
    You can refine claims based on feedback.''',
    verbose=True
)

# Agent 5: Description Writer
description_writer = Agent(
    role='Patent Specification Writer',
    goal='Write detailed patent specification and description',
    backstory='''Technical writer with patent experience.
    You write clear, detailed descriptions with proper sections:
    background, summary, detailed description, and drawings descriptions.
    You can revise based on reviewer feedback.''',
    verbose=True
)

# Agent 6: Patent Reviewer
reviewer = Agent(
    role='Patent Application Reviewer',
    goal='Review for completeness and quality, provide specific actionable feedback',
    backstory='''Senior patent prosecutor who reviews applications.
    You ensure all USPTO requirements are met, claims are defensible,
    and the specification fully supports the claims.
    You provide detailed, actionable feedback for revisions.''',
    verbose=True
)

# ============================================================================
# TASKS DEFINITION
# ============================================================================

def create_tasks(revision_feedback: str = None):
    """Create tasks with optional revision feedback context."""
    
    feedback_context = ""
    if revision_feedback:
        feedback_context = f"\n\nREVISION FEEDBACK TO ADDRESS:\n{revision_feedback}\n"
    
    task1 = Task(
        description=f'''Search for prior art related to: {{invention_description}}
        
        Use USPTO and Google Patents search tools specifically.
        Provide:
        - List of similar patents with specific patent numbers (US######)
        - Publication dates and inventors
        - Key technical differences from our invention
        - Patent classification codes (CPC/IPC)
        - Potential obstacles to patentability
        
        Be thorough and search multiple keyword combinations.{feedback_context}''',
        agent=prior_art_researcher,
        expected_output='Comprehensive prior art analysis with at least 5-10 relevant patents, including numbers, dates, and detailed comparison'
    )

    task2 = Task(
        description=f'''Analyze the technical aspects of: {{invention_description}}
        
        Identify:
        - Technical problem being solved
        - Technical solution provided
        - Key components and their interactions
        - Potential embodiments and variations
        - Technical advantages over prior art{feedback_context}''',
        agent=tech_analyzer,
        expected_output='Detailed technical breakdown with problem-solution analysis'
    )

    task3 = Task(
        description=f'''Based on prior art and technical analysis, assess novelty.
        
        Determine:
        - What elements are truly novel
        - What combinations are non-obvious
        - Strongest aspects for patent protection
        - Weaknesses to address
        - Recommended claim scope{feedback_context}''',
        agent=novelty_assessor,
        expected_output='Novelty assessment with specific protectable innovations identified'
    )

    task4 = Task(
        description=f'''Draft patent claims based on novelty assessment.
        
        Write:
        - 1-3 independent claims (broad to narrow)
        - 5-15 dependent claims (specific features)
        - Use proper claim language and structure
        - Ensure claims are supported by description
        - Number claims sequentially
        
        Format: "1. A method comprising: ..." or "1. A system comprising: ..."{feedback_context}''',
        agent=claims_writer,
        expected_output='Complete numbered set of patent claims in proper USPTO format'
    )

    task5 = Task(
        description=f'''Write the complete patent specification.
        
        Include all required sections:
        - Title (short, descriptive)
        - Field of invention (1-2 paragraphs)
        - Background (prior art problems, 2-3 paragraphs)
        - Summary of invention (key features, 2-3 paragraphs)
        - Brief description of drawings (if applicable)
        - Detailed description (comprehensive, multiple embodiments)
        - Abstract (150 words max)
        
        Ensure specification supports all claims.{feedback_context}''',
        agent=description_writer,
        expected_output='Complete patent specification with all required sections in proper format'
    )

    task6 = Task(
        description=f'''Review the complete patent application critically.
        
        Check:
        - Claims are properly supported by specification
        - All USPTO formal requirements met
        - Technical accuracy and completeness
        - Claim language is precise and defensible
        - No missing enablement details
        - Abstract meets 150-word limit
        
        Provide specific, actionable feedback for improvements.{feedback_context}''',
        agent=reviewer,
        expected_output='Detailed review report with specific recommendations and quality assessment'
    )
    
    return [task1, task2, task3, task4, task5, task6]

# ============================================================================
# MAIN EXECUTION WITH ITERATIVE REFINEMENT
# ============================================================================

def run_patent_generation(invention_description: str, max_iterations: int = 3):
    """Run the patent generation process with iterative refinement.
    
    Args:
        invention_description: Detailed description of the invention
        max_iterations: Maximum number of revision iterations
    """
    print("\n" + "=" * 80)
    print("PATENT APPLICATION GENERATION SYSTEM")
    print("=" * 80)
    print(f"\nStarting patent generation process...")
    print(f"Maximum iterations: {max_iterations}")
    
    iteration = 1
    revision_feedback = None
    approved = False
    
    while iteration <= max_iterations and not approved:
        print(f"\n{'='*80}")
        print(f"ITERATION {iteration} of {max_iterations}")
        print(f"{'='*80}\n")
        
        # Create tasks with feedback context
        tasks = create_tasks(revision_feedback)
        
        # Create Crew
        patent_crew = Crew(
            agents=[
                prior_art_researcher,
                tech_analyzer,
                novelty_assessor,
                claims_writer,
                description_writer,
                reviewer
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Run the crew
        print(f"\nRunning patent generation crew (Iteration {iteration})...")
        result = patent_crew.kickoff(inputs={
            'invention_description': invention_description
        })
        
        # Save raw output
        patent_data = export_sections_to_json(result, f"patent_data_iter_{iteration}.json")
        
        # Parse and structure the output
        result_str = str(result)
        structured_data = {
            'title': 'PATENT APPLICATION - AI GENERATED DRAFT',
            'iteration': iteration,
            'prior_art': result_str[:5000] if len(result_str) > 5000 else result_str,
            'field': 'Extracted from result...',
            'background': 'Generated based on prior art research...',
            'summary': 'Innovation summary...', 
            'detailed_description': result_str,  # Full result
            'claims': 'Claims section from result...',
            'abstract': 'Abstract summary...',
            'review_comments': 'Final section of result...'
        }
        
        # Export to DOCX
        docx_file = export_to_docx(structured_data, f"patent_application_iter_{iteration}.docx")
        
        print(f"\n{'='*80}")
        print(f"Iteration {iteration} Complete!")
        print(f"{'='*80}")
        print(f"\nGenerated files:")
        print(f"  - {docx_file}")
        print(f"  - output/patent_data_iter_{iteration}.json")
        
        # Human approval check
        approval_result = human_approval_check(structured_data, iteration)
        
        if approval_result['approved'] is True:
            approved = True
            print("\n" + "="*80)
            print("FINAL PATENT APPLICATION READY")
            print("="*80)
            print(f"\nFinal documents located in 'output' folder")
            print(f"\n⚠️  IMPORTANT DISCLAIMERS:")
            print(f"  - Have a patent attorney review before filing")
            print(f"  - Verify all prior art citations")
            print(f"  - Ensure technical accuracy")
            print(f"  - Consider provisional vs non-provisional filing")
            print(f"  - This is a DRAFT only, not legal advice")
            break
            
        elif approval_result['approved'] is False:
            revision_feedback = approval_result['feedback']
            iteration += 1
            print(f"\nPreparing iteration {iteration} with your feedback...")
            
        else:  # None - user chose to exit
            print("\nExiting patent generation process.")
            break
    
    if iteration > max_iterations and not approved:
        print(f"\n⚠️  Maximum iterations ({max_iterations}) reached.")
        print(f"Latest draft saved in 'output' folder.")
    
    return result

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example invention description
    invention_description = """
    A smart IoT-based home energy management system that uses machine learning
    to predict household energy consumption patterns and automatically optimize
    energy usage across multiple smart devices.
    
    Key features:
    - Real-time energy monitoring of individual appliances
    - ML-based prediction of future energy needs
    - Automatic load balancing across devices
    - Integration with renewable energy sources (solar panels)
    - User preferences learning system
    - Cost optimization algorithms
    - Grid demand-response participation
    
    Technical novelty:
    - Unlike existing systems that only monitor, this actively optimizes
    - Proprietary ML algorithm considers weather, occupancy, and user behavior
    - Novel load balancing technique that prevents power surges
    - Unique integration with local grid for demand-response programs
    
    Problem solved:
    - Reduces home energy costs by 20-30%
    - Prevents circuit overloads
    - Maximizes solar panel ROI
    - Reduces grid strain during peak hours
    """
    
    # Run the patent generation process
    result = run_patent_generation(
        invention_description=invention_description,
        max_iterations=3  # Allow up to 3 revision cycles
    )
