"""
Temporary development fixture data for the AgriTrial MVP.

This data is synthetic and is used only for backend development,
API testing, statistical testing, and dashboard integration.

It must not be treated as real trial data.

The production data source will later be replaced by the
AgriTrial SQLite/Supabase persistence layer.
"""
TRIAL_DATA = [
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Control",
        "metric": "nitrate",
        "value": 20.1
    },
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Control",
        "metric": "nitrate",
        "value": 21.7
    },
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Control",
        "metric": "nitrate",
        "value": 22.4
    },
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Treatment A",
        "metric": "nitrate",
        "value": 25.2
    },
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Treatment A",
        "metric": "nitrate",
        "value": 27.1
    },
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Treatment A",
        "metric": "nitrate",
        "value": 26.4
    } ,
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Treatment B",
        "metric": "nitrate",
        "value": 23.8
    },
    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Treatment B",
        "metric": "nitrate",
        "value": 24.6
    },

    {
        "trial_id": 1,
        "site": "Site A",
        "crop": "Tomato",
        "treatment": "Treatment B",
        "metric": "nitrate",
        "value": 25.1
    },
    {
        "trial_id": 2,
        "site": "Site B",
        "crop": "Tomato",
        "treatment": "Control",
        "metric": "nitrate",
        "value": 19.8
    },
    {
        "trial_id": 2,
        "site": "Site B",
        "crop": "Tomato",
        "treatment": "Control",
        "metric": "nitrate",
        "value": 20.6
    },
    {
        "trial_id": 2,
        "site": "Site B",
        "crop": "Tomato",
        "treatment": "Control",
        "metric": "nitrate",
        "value": 21.2
    },
    {
        "trial_id": 2,
        "site": "Site B",
        "crop": "Tomato",
        "treatment": "Treatment A",
        "metric": "nitrate",
        "value": 24.7
    },
    {
        "trial_id": 2,
        "site": "Site B",
        "crop": "Tomato",
        "treatment": "Treatment A",
        "metric": "nitrate",
        "value": 25.5
    },
    {
        "trial_id": 2,
        "site": "Site B",
        "crop": "Tomato",
        "treatment": "Treatment A",
        "metric": "nitrate",
        "value": 26.1
    }
]
