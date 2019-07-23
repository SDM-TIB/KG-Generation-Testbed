# Evaluation of relevant parameteres of a Knowledge Graph Construction 
This repository includes the resources to perform an evaluation over Knowledge Graph Construction Engines (RDFizers) to test how relevant parameters affect to the performance of these tools. 

## Contents
Folders:
- `data-generator` - contains one Jupyter Notebook for each parameter and the generate_data.py that generates the used data for 1k, 3k, 10k and 50k rows.
- `data` - Example the sample the generated data for 1k rows
- `mappings` - The RML mappings used to construct the Knowledge Graphs
- `results` - The corresponding results of the evaluation.


Scripts:
- `reproduce.sh` - shell script used to run the evaluation over the RMLMapper-java and SDM-RDFizer engines.



