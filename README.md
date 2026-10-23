# Factory Reallocation & Shipping Optimization Recommendation System

## Project Overview

This project analyzes shipping performance and factory-related data from the Nassau Candy Distributor dataset. It uses Python, machine learning, and geographic distance analysis to explore shipping lead times, product performance, factory performance, and possible factory-to-destination assignments.

The goal is to turn the available data into useful reports that can support decisions about shipping and factory allocation. The recommendations are preliminary and would need further validation before being used in a real supply chain.

## Project Objectives

- Analyze order and shipping data to understand delivery lead times.
- Prepare data for machine learning and compare different regression models.
- Study product and factory performance using sales, profit, units sold, and profit margins.
- Calculate approximate distances between candidate factories and selected customer destinations.
- Identify the nearest candidate factory for each selected destination.
- Generate CSV reports for further analysis and decision-making.

## Technologies Used

- **Python** — data analysis and implementation
- **Pandas and NumPy** — data handling and preprocessing
- **Scikit-learn** — machine learning models and evaluation
- **Matplotlib and Seaborn** — data visualization
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

### 5. Report Generation

The results are saved as CSV files so they can be reviewed, compared, and used in further analysis.

## Model Performance

The following are the recorded evaluation results from the project:

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 181.44 | 182.52 | 0.5290 |
| Random Forest | 148.36 | 177.16 | 0.5562 |
| Gradient Boosting | 159.58 | 169.53 | 0.5936 |

### Results and Interpretation

- **Linear Regression:** Provides a baseline for comparison.
- **Random Forest:** Achieves the lowest MAE among the three models.
- **Gradient Boosting:** Achieves the lowest RMSE and the highest R² among the evaluated models.

Based on these recorded metrics, Gradient Boosting performs best overall on RMSE and R², while Random Forest has the lowest MAE. Further validation would be needed before selecting a model for real-world use.

## Repository Contents

| File | Description |
|---|---|
| `Nassau_Candy_Distributor_Optimization.ipynb` | Notebook containing the analysis and implementation |
| `factory_destination_distances.csv` | Distance estimates between candidate factories and selected destinations |
| `factory_performance_summary.csv` | Summary of factory-level performance |
| `factory_recommendations.csv` | Product-to-factory mappings and preliminary recommendations |
| `model_comparison.csv` | Comparison of regression model evaluation metrics |
| `nearest_factory_assignments.csv` | Nearest candidate factory for each selected destination |
| `product_summary.csv` | Product-level performance summary |
| `single_factory_distance_comparison.csv` | Distance comparison for the single-factory scenario |

## Limitations

- The dataset contains date inconsistencies and unusually long shipping lead times that may affect model performance.
- Some order IDs and order dates appear inconsistent and require further validation.
- The product-to-factory assignments are predefined rather than produced by an optimization algorithm.
- Factory coordinates are assumed and have not been verified.
- Straight-line distances do not represent actual road routes, shipping costs, or delivery times.
- The geographic analysis covers 15 selected destinations, not necessarily every customer location.
- The current analysis does not fully account for factory capacity, inventory, production cost, transportation cost, or operational constraints.

## Future Improvements

- Validate order dates, order IDs, and unusually long lead times.
- Improve feature engineering and use more systematic model validation.
- Verify factory and destination coordinates.
- Incorporate actual transportation routes and shipping costs.
- Develop an optimization model that considers factory capacity, inventory, demand, and production constraints.
- Build an interactive dashboard to explore model results and factory recommendations.

## Conclusion

This project combines data analysis, regression modelling, factory performance summaries, and geographic distance calculations to explore possible improvements in shipping and factory allocation.

The current results provide a starting point for further investigation. More reliable data, verified locations, and operational constraints would be needed to develop a practical factory-reallocation and shipping optimization system.

## Disclaimer

This project is for educational and analytical purposes. Its predictions and recommendations are preliminary and should not be treated as validated operational decisions.
