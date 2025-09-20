# src/tutorials/prometheus.py

TUTORIAL_CATEGORY = "Prometheus: Monitoring"

TUTORIALS = {
    "prometheus_1_1": {
        "name": "Introduction to Prometheus",
        "description": "Learn the basics of Prometheus and its configuration file.",
        "skills_learned": [
            "Understanding the basics of Prometheus",
            "Understanding the Prometheus configuration file"
        ],
        "steps": [
            {
                "text": "Welcome to the Prometheus tutorial!\n\nPrometheus is an open-source monitoring and alerting toolkit. It collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "Prometheus is configured via a YAML file. The configuration file specifies everything related to scraping, as well as rule files.\n\nLet's take a look at a simple Prometheus configuration file.\n\nType `cat prometheus.yml` to see the configuration file.",
                "expected_command": "cat prometheus.yml"
            },
            {
                "text": "This configuration file tells Prometheus to scrape a single target, the Prometheus server itself. The `scrape_interval` is set to 15 seconds, which means that Prometheus will scrape the target every 15 seconds.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "type": "mcq",
                "text": "What is the purpose of the `scrape_interval` setting in the Prometheus configuration file?",
                "answers": [
                    "a) It specifies how often to evaluate rules.",
                    "b) It specifies how often to scrape targets.",
                    "c) It specifies the port on which to expose metrics."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You have successfully learned the basics of Prometheus!"
            }
        ]
    },
    "prometheus_1_2": {
        "name": "Monitoring a Target with an Exporter",
        "description": "Learn how to monitor a target with an exporter in Prometheus.",
        "skills_learned": [
            "Understanding the role of exporters in Prometheus",
            "Configuring Prometheus to scrape a target with an exporter"
        ],
        "steps": [
            {
                "text": "Prometheus scrapes metrics from instrumentalized jobs, either directly or via an intermediary push gateway for short-lived jobs. It stores all scraped samples locally and runs rules over this data to either aggregate and record new time series from existing data or generate alerts.\n\nSometimes it is not feasible to instrument a given system with Prometheus metrics directly. This is where exporters come in. Exporters are helper services that can take data from other systems and export it in a format that Prometheus can understand.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "In this tutorial, we will use the Node Exporter to expose metrics from our local machine. The Node Exporter is a popular exporter that provides a wide range of system-level metrics.\n\nLet's add the Node Exporter to our Prometheus configuration file. Type `edit-prometheus-config` to open the configuration file.",
                "expected_command": "edit-prometheus-config"
            },
            {
                "text": "Now, add the following to the end of the file to configure Prometheus to scrape the Node Exporter:\n\n```yaml\n  - job_name: 'node'\n    static_configs:\n      - targets: ['localhost:9100']\n```\n\nType `END` on a new line to finish editing the file.",
                "expected_command": "END"
            },
            {
                "text": "Now that you have configured Prometheus to scrape the Node Exporter, you can restart Prometheus to apply the changes. In a real environment, you would restart the Prometheus service. For this tutorial, we will simulate this by typing `restart-prometheus`.",
                "expected_command": "restart-prometheus"
            },
            {
                "type": "mcq",
                "text": "What is the purpose of an exporter in Prometheus?",
                "answers": [
                    "a) To visualize metrics in a dashboard.",
                    "b) To convert metrics from other systems into a format that Prometheus can understand.",
                    "c) To send alerts to a notification channel."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You have successfully configured Prometheus to monitor a target with an exporter!"
            }
        ]
    }
}
