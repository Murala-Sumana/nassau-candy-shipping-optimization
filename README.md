# Factory Reallocation & Shipping Optimization Recommendation System

An exploratory decision-support project for **Nassau Candy Distributor**, built with Python, machine learning, geographic distance analysis, and an interactive Streamlit dashboard.

**Live Dashboard:** https://candy-data-dashboard.streamlit.app/

## Project Overview

This project analyzes shipping performance and factory-related data from the Nassau Candy Distributor dataset (approximately 10,194 records). It uses Python, machine learning, and geographic distance analysis to explore shipping lead times, product performance, factory performance, and possible factory-to-destination assignments.

The goal is to turn the available data into useful reports and an interactive dashboard that can support decisions about shipping and factory allocation. The recommendations are preliminary and would need further validation before being used in a real supply chain.

## Project Objectives

- Analyze order and shipping data to understand delivery lead times.
- Prepare data for machine learning and compare different regression models.
- Study product and factory performance using sales, profit, units sold, and profit margins.
- Calculate approximate distances between candidate factories and selected customer destinations.
- Identify the nearest candidate factory for each selected destination.
- Compare current and proposed factory assignments with what-if scenario analysis.
- Generate CSV reports and an interactive dashboard for further analysis and decision-making.

## Technologies Used

- **Python** — data analysis and implementation
- **Pandas and NumPy** — data handling and preprocessing
- **Scikit-learn** — machine learning models and evaluation
- **Matplotlib and Seaborn** — data visualization in the notebook
- **Streamlit** — interactive dashboard
- **Google Colab** — development and analysis
- **GitHub** — project version control and sharing

## Project Workflow

### 1. Data Loading and Preprocessing

The dataset is loaded and inspected to understand its structure, identify relevant columns, and prepare the data for analysis.

### 2. Shipping Lead-Time Prediction

Regression models are used to estimate shipping lead times based on selected order, product, and shipping-related features.

The models evaluated are:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Model performance is compared using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and the coefficient of determination (R²).

### 3. Product and Factory Performance Analysis

Product and factory summaries are created to examine sales, profit, units sold, and profit margins.

The project uses predefined product-to-factory mappings to organize the analysis. Products with profit margins below 20% are flagged for review. These are preliminary, rule-based recommendations rather than the results of a fully optimized factory-allocation algorithm.

### 4. Geographic Distance Analysis

Approximate straight-line distances are calculated between five candidate factories and 15 selected customer destinations.

The analysis identifies the nearest candidate factory for each selected destination and compares distances for a single-factory scenario.

Factory coordinates are assumed for this analysis and should be verified before practical use.

### 5. Interactive Dashboard

The results are brought together in a Streamlit dashboard, where users can explore factory performance, product summaries, distance comparisons, recommendations, and what-if scenarios.

The what-if analysis compares a current and a proposed factory using:

`Distance Difference = Current Distance − Proposed Distance`

A positive value means the proposed factory is closer, a negative value means it is farther away, and zero means the distances are equal. This measures straight-line distance only and does not predict delivery time, shipping cost, or profit.

### 6. Report Generation

The results are saved as CSV files so they can be reviewed, compared, and used in further analysis.

## Dashboard

**Live app:** https://candy-data-dashboard.streamlit.app/

To run it locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard includes the following sections:

1. Overview
2. Factory Optimization Simulator
3. What-If Scenario Analysis
4. Recommendation Dashboard
5. Risk & Impact Panel
6. Factory recommendations
7. Factory performance
8. Product summary
9. Model comparison
10. Factory–destination distances
11. Nearest-factory assignments
12. Single-factory comparison
13. Raw Data Explorer
14. About & Limitations

Tables can be searched and filtered, and the prepared outputs can be downloaded.

## Model Performance

The following are the recorded evaluation results from the project:

| Model             | MAE (days) | RMSE (days) | R²     |
|-------------------|-----------:|------------:|-------:|
| Linear Regression |     181.44 |      182.52 | 0.5290 |
| Random Forest     |     148.36 |      177.16 | 0.5562 |
| Gradient Boosting |     159.58 |      169.53 | 0.5936 |

### Results and Interpretation

- **Linear Regression:** Provides a baseline for comparison.
- **Random Forest:** Achieves the lowest MAE among the three models.
- **Gradient Boosting:** Achieves the lowest RMSE and the highest R² among the evaluated models.

Based on these recorded metrics, Gradient Boosting performs best overall on RMSE and R², while Random Forest has the lowest MAE. The errors are large when expressed in days and the source dates are inconsistent, so further validation would be needed before selecting a model for real-world use.

## Repository Contents

| File                                          | Description                                                              |
|-----------------------------------------------|--------------------------------------------------------------------------|
| `Nassau Candy Distributor (3).csv`            | Original source dataset                                                  |
| `Nassau_Candy_Distributor_Optimization.ipynb` | Notebook containing the analysis and implementation                      |
| `app.py`                                      | Streamlit dashboard application                                          |
| `requirements.txt`                            | Python packages required to run the project                              |
| `factory_destination_distances.csv`           | Distance estimates between candidate factories and selected destinations |
| `factory_performance_summary.csv`             | Summary of factory-level performance                                     |
| `factory_recommendations.csv`                 | Product-to-factory mappings and preliminary recommendations              |
| `model_comparison.csv`                        | Comparison of regression model evaluation metrics                        |
| `nearest_factory_assignments.csv`             | Nearest candidate factory for each selected destination                  |
| `product_summary.csv`                         | Product-level performance summary                                        |
| `single_factory_distance_comparison.csv`      | Distance comparison for the single-factory scenario                      |

## Limitations

- The dataset contains date inconsistencies and unusually long shipping lead times that may affect model performance.
- Some order IDs and order dates appear inconsistent and require further validation.
- The product-to-factory assignments are predefined rather than produced by an optimization algorithm.
- Factory coordinates are assumed and have not been verified.
- Straight-line distances do not represent actual road routes, shipping costs, or delivery times.
- The geographic analysis covers 15 selected destinations, not necessarily every customer location.
- The current analysis does not fully account for factory capacity, inventory, production cost, transportation cost, or operational constraints.
- No transportation-cost savings, faster deliveries, or profit improvements are established by this project.

## Future Improvements

- Validate order dates, order IDs, and unusually long lead times.
- Improve feature engineering and use more systematic model validation.
- Verify factory and destination coordinates.
- Incorporate actual transportation routes and shipping costs.
- Develop an optimization model that considers factory capacity, inventory, demand, and production constraints.
- Extend the dashboard with verified route-level and cost data.

## Conclusion

This project combines data analysis, regression modelling, factory performance summaries, geographic distance calculations, and an interactive dashboard to explore possible improvements in shipping and factory allocation.

The current results provide a starting point for further investigation. More reliable data, verified locations, and operational constraints would be needed to develop a practical factory-reallocation and shipping optimization system.

## Disclaimer

This project is for educational and analytical purposes. Its predictions and recommendations are preliminary and should not be treated as validated operational decisions.
