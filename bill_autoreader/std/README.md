## Tariff Standardization

### Background

In the energy market, comparing tariff structures across various retailers is crucial to identify the best pricing and optimize customer savings. The inconsistencies in tariff naming conventions across different retailer companies make it challenging to compare rates directly. This standardization system was developed to bridge that gap by providing a unified way to identify and categorize tariffs, enabling better decision-making.

### Goal of the module

- Standardization: Create clear tariff categories that encompass different naming patterns across energy retailers.
- Generalization: Recognize familiar tariff names and smartly categorize new or unseen names by learning from existing patterns. This ensures new names are classified accurately.
- Flexibility: Quickly add or modify patterns as more tariff names are discovered from different retailers.
- Scalability: Handle a growing list of retailers by allowing easy updates.
- Robustness & Maintanibility: Automated tests ensure that updates or additions don't interfere with existing functionality, preventing changes that could disrupt tariff identification.

### Adding New Tariff Names

#### 1. Add Tariff Names

go to : bill_autoreader/std/retailer.py

If there are tariff names that need to be correctly classified, add them to the appropriate retailer. If the retailer doesn't yet exist, create a new variable to compile the various tariffs from that retailer, then add this variable to RETAILERS_TARIFFS. If the retailer already exists, simply add the tariff names and specify the standardized tariff category they should belong to.

#### 2. Testing and Validation

run unit tests : pytest tests/test_std.py::test_identify_tariffs_found -vv

If it passes the test, then it is complete; we already know that the tariffs will be classified correctly.

if it doesnt passed the test, then we need to develop the pattern.

#### 3. Develop Pattern

Create regex patterns that accurately capture the key elements while excluding irrelevant terms. Add these patterns to the correct category. Then, rerun the tests until all are passed.

### Unknown Tariff Names

Unknown tariff names are those not categorized into any specific category. By default, these should be labeled as 'additional.'
