###  Project Summary: IaaS [CSE 546] [SPRING_2024] Cloud Computing

#### **Project Overview:**
This project focused on developing an elastic face recognition application using AWS IaaS resources, emphasizing automatic scaling and cost-effectiveness. The project involved creating a web tier and integrating app and data tiers to form a complete multi-tiered architecture.

#### **Tasks Completed:**


1. **EC2 Instances Creation:**
   - **Security Credentials:** Defined and managed security credentials.
   - **Key Pairs and SSH:** Created key pairs and set SSH inbound rules for secure instance access.
   - **EC2 Instance Setup:** Launched and configured an EC2 instance using a specified Ubuntu AMI, and assigned it an Elastic IP for consistent access.

2. **Web Tier Development:**
   - **HTTP POST Handling:** Implemented a web service to handle image uploads for face recognition using a lookup table.
   - **Concurrent Request Management:** Ensured the web tier could manage multiple concurrent requests efficiently.
   - **Testing:** Validated functionality using a provided workload generator, ensuring the correct handling and output of recognition results.

3. **App Tier Development:**
   - **App Tier Instances:** Created AMIs and launched app tier instances, implementing custom autoscaling to adjust instance numbers based on demand. Implemented queues using SQS to buffer requests and decouple the architecture.

4. **Data Tier Implementation:**
   - **S3 Buckets:** Utilized S3 for storing input images and recognition results with specific naming conventions.
   - **Data Persistence:** Ensured correct mapping and persistence of data between tiers.

5. **System Validation and Testing:**
   - **Functionality Testing:** Used automated scripts to thoroughly test the web tier and integrated application.
   - **AWS Usage Monitoring:** Monitored AWS usage to prevent unnecessary charges.
   - **Workload Testing:** Tested the application with 10, 50, 100, and 1000 concurrent requests to ensure scalability and accuracy.
   - **Latency Requirements:** Ensured the application met specified latency requirements.


#### **Skills and Techniques Acquired:**
This project enhanced my ability to utilize AWS IaaS resources for building scalable, reliable cloud applications, laying a strong foundation for future cloud-based development projects.
