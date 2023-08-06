define([],
    function () {
        return {
            // connection dialog
            connection: {
                name: null,
                dto: null,
                candidateName: null,
                candidateDTO: null
            },

            // upload dialog
            uploadDataSetType: null,
            uploadDataSetTypes: {},
            uploadEntity: null,
            datasetCheckboxes: [],
            fileCheckboxes: [],
            selectedFiles: [],
            unselectedDatasets: [],

            // download dialog
            selectedDatasets: new Set([]),
            entity: null,
            workingDirectory: '',

            // openBIS v3 connection
            openbisService : null
        }
    }
)