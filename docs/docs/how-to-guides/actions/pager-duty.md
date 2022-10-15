---
sidebar_position: 3
slug: ./pagerduty
---

# PagerDuty

## How to create a PagerDuty Destination & Action
![](/img/actions/pagerduty/example.png)

#### Step 1. Navigate to the `Services` tab, then click on your service.

![](/img/actions/pagerduty/step-1.png)

#### Step 2. Click on `Integrations` followed by `Add integration`

![](/img/actions/pagerduty/step-2.png)

#### Step 3. Select the `Events API V2` integration, then click `Add`.

![](/img/actions/pagerduty/step-3.png)

#### Step 4. Click on the new integration and copy the `Integration Key`. Make note of the `region` in the `Integration URL`. If it is `eu`, you will need to specify `eu` as the region. If one does not exist, you will use `us` as the region.

![](/img/actions/pagerduty/step-4.png)

#### Step 5. Navigate to [http://127.0.0.1:3000/destinations/home](http://127.0.0.1:3000/destinations/home) and click `+ Destination`
![](/img/create-destination.png)

#### Step 5. Fill in the details for the destination as shown below and then click `Create`. (Remember to select the correct region)
:::tip
Swiple supports AWS Secret Manager, GCP Secret Manager, and Azure Key Vault. Instead of using a raw secret, replace it with the path/name of the secret.
For more information, see [How to use AWS Secret Manager, GCP Secret Manager, & Azure Key Vault](/docs/configuration/secrets-manager)
:::
![](/img/actions/pagerduty/step-5.png)

#### Step 6. Navigate to the dataset you'd like to add an Action to, click the `Actions` tab, then click `+ Action`.
![](/img/dataset-create-action.png)

#### Step 7. Configure your Action and then click `Create`.
![](/img/actions/pagerduty/step-6.png)

#### You're Done! 🎉
