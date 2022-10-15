---
sidebar_position: 4
slug: ./microsoft-teams
---

# Microsoft Teams

## How to create a Microsoft Teams Destination & Action

![](/img/actions/microsoftteams/example.png)

#### Step 1. Find the channel you would like to receive Swiple notifications in. Click the `3 dots`, then click on `Connectors`.
![](/img/actions/microsoftteams/step-1.png)

#### Step 2. Find `Incoming Webhook` and click on `Configure`.
![](/img/actions/microsoftteams/step-2.png)

#### Step 3. Provide a name for the connector, we used `Swiple`. Download the Swiple logo below and upload it to your connector, then click `Create`.
<a target="\_blank" href={require('/img/actions/microsoftteams/swiple-ms-teams-connector.png').default}> Download Swiple Logo </a>

![](/img/actions/microsoftteams/step-3.png)

#### Step 4. Copy your webhook URL and click `Done`.
![](/img/actions/microsoftteams/step-4.png)

#### Step 5. Navigate to [http://127.0.0.1:3000/destinations/home](http://127.0.0.1:3000/destinations/home) and click `+ Destination`
![](/img/create-destination.png)

#### Step 6. Fill in the details for the destination as shown below and then click `Create`.
:::tip
Swiple supports AWS Secret Manager, GCP Secret Manager, and Azure Key Vault. Instead of using a raw secret, replace it with the path/name of the secret.
For more information, see [How to use AWS Secret Manager, GCP Secret Manager, & Azure Key Vault](/docs/how-to-guides/secrets-manager)
:::
![](/img/actions/microsoftteams/step-5.png)

#### Step 7. Navigate to the dataset you'd like to add an Action to, click the `Actions` tab, then click `+ Action`.
![](/img/dataset-create-action.png)

#### Step 8. Configure your Action and then click `Create`.
![](/img/actions/microsoftteams/step-6.png)

#### You're Done! 🎉
