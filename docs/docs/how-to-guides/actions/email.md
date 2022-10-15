---
sidebar_position: 5
slug: ./email
---

# Email

## How to create an Email Destination & Action with Amazon SES

![](/img/actions/email/example.png)

#### Step 1. Go to the AWS Console and navigate to `Amazon Simple Email Service`.
![](/img/actions/email/step-1.png)

#### Step 2. In the side-bar, click `SMTP Settings` followed by `Create SMTP credentials`.
![](/img/actions/email/step-2.png)

#### Step 3. You will be presented with and IAM User that needs to be created. Provide a name and then click `Create`.
![](/img/actions/email/step-3.png)

#### Step 4. Click `Show User SMTP Security Credentials` and save them somewhere private and secure.
![](/img/actions/email/step-4.png)

#### Step 5. Navigate to [http://127.0.0.1:3000/destinations/home](http://127.0.0.1:3000/destinations/home) and click `+ Destination`
![](/img/create-destination.png)

#### Step 6. Fill in the details for the destination as shown below and then click `Create`.
:::tip
Swiple supports AWS Secret Manager, GCP Secret Manager, and Azure Key Vault. Instead of using a raw secret, replace it with the path/name of the secret.
For more information, see [How to use AWS Secret Manager, GCP Secret Manager, & Azure Key Vault](/docs/how-to-guides/secrets-manager)
:::
![](/img/actions/email/step-5.png)

#### Step 7. Navigate to the dataset you'd like to add an Action to, click the `Actions` tab, then click `+ Action`.
![](/img/dataset-create-action.png)

#### Step 8. Configure your Action and then click `Create`.
![](/img/actions/email/step-6.png)

#### You're Done! 🎉
