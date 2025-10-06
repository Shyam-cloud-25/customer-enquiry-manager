# 🧠 Customer Enquiry Manager – AWS AI Project

A fully functional cloud application built using **AWS Services** that automates customer enquiry handling.

---

## 🚀 Architecture Overview

**Frontend:** S3 Static Website  
**Backend:** EC2 Flask API  
**AI Layer:** Amazon Bedrock (Titan G1 Lite)  
**Database:** DynamoDB  
**Email Automation:** Amazon SES  

Data Flow:
1. User submits enquiry on the S3 web form.
2. EC2 Flask API stores the record in DynamoDB.
3. Bedrock classifies the query (Billing / Technical / General).
4. SES sends an automated confirmation email.

---

## 🧰 AWS Services Used
- Amazon EC2  
- Amazon DynamoDB  
- Amazon SES  
- Amazon Bedrock  
- Amazon S3  
- IAM Roles & Policies  
- CloudWatch (optional monitoring)

---

## 🧪 Testing
✅ Form Submission → Stored in DynamoDB  
✅ Email → Delivered via SES  
✅ Bedrock → Correctly classifies enquiry type  

---

## 🧾 Screenshots
All setup and testing screenshots are under the screenshot folder.

---

## 👤 Author
**Project by:** Shyam  
**Region:** ap-south-1 (Mumbai)

---

## 🧹 Cleanup (Important)
To avoid AWS charges:
1. Terminate EC2 instance  
2. Delete S3 bucket  
3. Delete DynamoDB table  
4. Delete SES verified identities  
5. Delete Bedrock model access (optional)  
6. Detach IAM policies & remove test roles  

---

⭐ *A great resume project demonstrating AWS + AI + DevOps integration.*
