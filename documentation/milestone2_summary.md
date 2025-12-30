# Milestone 2 – Machine Learning Model Development
**Name:** Lokesh Patil  
**Branch:** Springboard_01  

## Objective
To build and evaluate machine learning models for predicting packaging material cost and CO₂ footprint and generate an initial recommendation ranking.

## Dataset Preparation
- Used cleaned dataset from Module 2.
- Selected material strength, load capacity, biodegradability, and recyclability as input features.
- Defined two target variables: cost per kg and CO₂ emission score.
- Split dataset into training (80%) and testing (20%).
- Applied standard scaling for feature normalization.

## Model Development
- Implemented Random Forest regression models for cost and CO₂ prediction.
- Implemented XGBoost regression model for cost prediction to compare performance.

## Model Evaluation
- Evaluated models using RMSE, MAE, and R² metrics.
- Validated predictions using actual vs predicted graphs.

## Material Recommendation
- Generated predicted cost and CO₂ values for all materials.
- Computed a material suitability score favoring low cost and low CO₂ impact.
- Ranked materials based on the suitability score.

## Outcome
- Successfully built an end-to-end ML pipeline.
- Produced interpretable predictions and initial material recommendations to support sustainable packaging decisions.
