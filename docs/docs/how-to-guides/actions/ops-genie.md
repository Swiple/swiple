---
sidebar_position: 1
slug: ./opsgenie
---

# OpsGenie

## How to create an OpsGenie Destination & Action

![](/img/actions/opsgenie/example.png)

#### Step 1. Navigate to the `Teams` tab, then click your team name.
![](/img/actions/opsgenie/step-1.png)

#### Step 2. Click on `Integrations` followed by `Add integration`
![](/img/actions/opsgenie/step-2.png)

#### Step 3. Click on the `API` integration, copy your API Key and then click `Save integration`.
![](/img/actions/opsgenie/step-3.png)

#### Step 4. Navigate to [http://127.0.0.1:3000/destinations/home](http://127.0.0.1:3000/destinations/home) and click `+ Destination`
![](/img/create-destination.png)

#### Step 5. Fill in the details for the destination as shown below and then click `Create`.
:::tip
Swiple supports AWS Secret Manager, GCP Secret Manager, and Azure Key Vault. Instead of using a raw secret, replace it with the path/name of the secret.
For more information, see [How to use AWS Secret Manager, GCP Secret Manager, & Azure Key Vault](/docs/how-to-guides/secrets-manager)
:::
![](/img/actions/opsgenie/step-5.png)

#### Step 6. Navigate to the dataset you'd like to add an Action to, click the `Actions` tab, then click `+ Action`.
![](/img/dataset-create-action.png)

#### Step 7. Configure your Action and then click `Create`.
![](/img/actions/opsgenie/step-6.png)


#### You're Done! 🎉
