# Databricks notebook source
# MAGIC %md
# MAGIC # Setup Sample Data
# MAGIC 
# MAGIC This notebook creates sample data tables for the MCP workshop demonstrations.

# COMMAND ----------

# MAGIC %python
# MAGIC 
# MAGIC import pandas as pd
# MAGIC import numpy as np
# MAGIC from datetime import datetime, timedelta
# MAGIC 
# MAGIC # Get parameters
# MAGIC catalog_name = dbutils.widgets.get("catalog_name") if "dbutils" in globals() else "mcp_workshop"
# MAGIC 
# MAGIC print(f"Setting up sample data in catalog: {catalog_name}")
# MAGIC 
# MAGIC # Set the catalog context
# MAGIC spark.sql(f"USE CATALOG {catalog_name}")
# MAGIC spark.sql(f"USE SCHEMA default")
# MAGIC print(f"✅ Using catalog: {catalog_name}.default")

# COMMAND ----------

# MAGIC %python
# MAGIC 
# MAGIC # Generate sample products data
# MAGIC np.random.seed(42)
# MAGIC 
# MAGIC products_data = {
# MAGIC     'product_id': [f'P{str(i).zfill(3)}' for i in range(1, 101)],
# MAGIC     'product_name': [f'Product {chr(65 + i % 26)}{i}' for i in range(1, 101)],
# MAGIC     'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], 100),
# MAGIC     'price': np.round(np.random.uniform(10, 500, 100), 2),
# MAGIC     'description': [f'High-quality product for {category.lower()} enthusiasts' 
# MAGIC                    for category in np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], 100)]
# MAGIC }
# MAGIC 
# MAGIC products_df = pd.DataFrame(products_data)
# MAGIC 
# MAGIC # Create Spark DataFrame and save as Delta table
# MAGIC products_spark_df = spark.createDataFrame(products_df)
# MAGIC products_spark_df.write.mode("overwrite").saveAsTable(f"{catalog_name}.default.products")
# MAGIC 
# MAGIC print("✅ Created products table")

# COMMAND ----------

# MAGIC %python
# MAGIC 
# MAGIC # Generate sample customers data
# MAGIC customers_data = {
# MAGIC     'customer_id': [f'C{str(i).zfill(4)}' for i in range(1, 501)],
# MAGIC     'customer_name': [f'Customer {i}' for i in range(1, 501)],
# MAGIC     'email': [f'customer{i}@example.com' for i in range(1, 501)],
# MAGIC     'region': np.random.choice(['North', 'South', 'East', 'West'], 500),
# MAGIC     'signup_date': [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(500)]
# MAGIC }
# MAGIC 
# MAGIC customers_df = pd.DataFrame(customers_data)
# MAGIC customers_spark_df = spark.createDataFrame(customers_df)
# MAGIC customers_spark_df.write.mode("overwrite").saveAsTable(f"{catalog_name}.default.customers")
# MAGIC 
# MAGIC print("✅ Created customers table")

# COMMAND ----------

# MAGIC %python
# MAGIC 
# MAGIC # Generate sample sales data
# MAGIC sales_data = []
# MAGIC for i in range(1000):
# MAGIC     sales_data.append({
# MAGIC         'sale_id': f'S{str(i).zfill(5)}',
# MAGIC         'customer_id': f'C{str(np.random.randint(1, 501)).zfill(4)}',
# MAGIC         'product_id': f'P{str(np.random.randint(1, 101)).zfill(3)}',
# MAGIC         'quantity': np.random.randint(1, 5),
# MAGIC         'sale_date': datetime.now() - timedelta(days=np.random.randint(1, 90)),
# MAGIC         'revenue': np.round(np.random.uniform(20, 1000), 2)
# MAGIC     })
# MAGIC 
# MAGIC sales_df = pd.DataFrame(sales_data)
# MAGIC sales_spark_df = spark.createDataFrame(sales_df)
# MAGIC sales_spark_df.write.mode("overwrite").saveAsTable(f"{catalog_name}.default.sales")
# MAGIC 
# MAGIC print("✅ Created sales table")

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC -- Verify the tables were created
# MAGIC SHOW TABLES IN ${catalog_name}.default;

# COMMAND ----------

# MAGIC %python
# MAGIC 
# MAGIC print("✅ Sample data setup complete!")
# MAGIC print(f"Created tables in {catalog_name}.default:")
# MAGIC print("  - products (100 rows)")
# MAGIC print("  - customers (500 rows)") 
# MAGIC print("  - sales (1000 rows)")
# MAGIC print("Ready for MCP demonstrations!")
