---
sidebar_position: 2
slug: ./slack
---

# Slack

## How to create a Slack Destination & Action
![](/img/actions/slack/example.png)

#### Step 1. Navigate to [Sending messages using Incoming Webhooks](https://api.slack.com/messaging/webhooks#) and click `Create your slack app`.

#### Step 2. A modal will appear (if not, click `Create New App`), click `From scratch`
![](/img/actions/slack/step-2.png)

#### Step 3. Enter an App Name of `Swiple Webhook`, select your workspace, then click `Create App`
![](/img/actions/slack/step-3.png)

#### Step 4. Click `Incoming Webhooks`
![](/img/actions/slack/step-4.png)

#### Step 5. Turn Activate Incoming Webhooks `On` and then click `Add New Webhook to Workspace`
![](/img/actions/slack/step-5.png)

#### Step 6. Select your channel and click `Allow`
![](/img/actions/slack/step-6.png)

#### Step 7. Copy your Webhook URL, it should start with `https://hooks.slack.com/services/`
![](/img/actions/slack/step-7.png)

#### Step 8. Navigate to [http://127.0.0.1:3000/destinations/home](http://127.0.0.1:3000/destinations/home) and click `+ Destination`
![](/img/create-destination.png)

#### Step 9. Fill in the details for the destination as shown below and then click `Create`.
:::tip
Swiple supports AWS Secret Manager, GCP Secret Manager, and Azure Key Vault. Instead of using a raw secret, replace it with the path/name of the secret.
For more information, see [How to use AWS Secret Manager, GCP Secret Manager, & Azure Key Vault](/docs/how-to-guides/secrets-manager)
:::
![](/img/actions/slack/step-8.png)

#### Step 10. Navigate to the dataset you'd like to add an Action to, click the `Actions` tab, then click `+ Action`.
![](/img/dataset-create-action.png)

#### Step 11. Configure your Action and then click `Create`.
![](/img/actions/slack/step-9.png)


#### You're Done! 🎉
