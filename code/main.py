from default_workflow import DefaultWorkflow

if __name__ == '__main__':
    # Create a workflow
    workflow = DefaultWorkflow()
    # Generate the seed
    inputs = workflow.generate_input()
    # Do one pass
    first_pass = workflow.run(inputs, save=True)
    generated_facts = first_pass.get_generated_facts()
    # print
    for generated_fact in generated_facts:
        print(generated_fact.get_subject().get(), ",",
              generated_fact.get_predicate().get(), ",",
              generated_fact.get_object().get(), ",",
              generated_fact.get_score())
