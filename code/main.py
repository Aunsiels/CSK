from default_workflow import DefaultWorkflow

if __name__ == '__main__':
    workflow = DefaultWorkflow()
    inputs = workflow.generate_input()
    first_pass = workflow.run(inputs)
    generated_facts = first_pass.get_generated_facts()
