# Validation and Error Handling Standard

## Purpose

Sarateal uses a centralized validation and exception-handling pattern so that errors are predictable, readable, and safe for API users, dashboard users, and future automated jobs.

The goal is to avoid scattered raw exceptions such as database errors, Python tracebacks, or unclear validation failures.

## Core principle

All expected application errors should be raised as Sarateal application exceptions.

These exceptions live in:

```text
app/core/exceptions.py

FastAPI handles them once through:

app/core/exception_handlers.py

This means services can focus on business rules, while the API layer returns consistent error responses.

Error response shape

Every handled application error should return this structure:

{
  "error": {
    "code": "DUPLICATE_RECORD",
    "message": "Farmer already exists.",
    "details": [
      {
        "field": "phone_number",
        "message": "A farmer with this phone_number already exists.",
        "value": "0700000001"
      }
    ],
    "context": {
      "entity": "Farmer",
      "field": "phone_number"
    }
  }
}
Main error categories
VALIDATION_ERROR

Used when incoming API data fails schema validation before reaching the service layer.

Example:

Missing required field
Wrong data type
Invalid request body
DUPLICATE_RECORD

Used when a user tries to create a record that already exists.

Examples:

Farmer with the same phone number
Buyer with the same name
Product with the same name
County with the same code
RECORD_NOT_FOUND

Used when a referenced record does not exist.

Examples:

Creating supply for a farmer_id that does not exist
Creating demand for a buyer_id that does not exist
Creating tender for a product_id that does not exist
BUSINESS_RULE_VIOLATION

Used when the request is technically valid, but violates Sarateal business logic.

Examples:

Supply quantity is zero
Demand date ends before it starts
Tender closing date is earlier than opening date
Opportunity score is outside 0–100
DATA_INTEGRITY_ERROR

Used when the database rejects an operation.

Examples:

Unique constraint failure
Foreign key issue
Invalid relationship

This is a safety net. Ideally, service validation should catch these before the database does.

EXTERNAL_SOURCE_ERROR

Reserved for future data-source jobs.

Examples:

Tender source unavailable
Price feed failed
Climate data pull failed
Invalid external API response
UNAUTHORIZED_ACTION

Reserved for future user roles and permissions.

Examples:

Buyer trying to edit another buyer profile
County user trying to access another county dashboard
Unverified user trying to publish official supply
INTERNAL_ERROR

Used only for unexpected failures.

This should never expose sensitive stack traces to users.

Validation layers

Sarateal uses layered validation.

1. Schema validation

Handled by Pydantic schemas in:

app/schemas/

This validates basic data shape.

Examples:

Required fields
String fields
Date fields
Integer IDs
Boolean flags
2. Service validation

Handled in service files in:

app/services/

This validates business rules.

Examples:

Farmer must exist before supply is created
Product must exist before demand is created
Supply quantity must be positive
Demand timing must make sense
Tender URL must be valid
3. Database validation

Handled by SQLAlchemy and database constraints.

Examples:

Unique values
Non-null fields
Foreign key relationships

This should be the final guardrail, not the first line of defense.

Current validation coverage
Farmers

File:

app/services/farmers.py

Rules:

Duplicate phone numbers are blocked.
Farmer lookup can raise RECORD_NOT_FOUND.
Buyers

File:

app/services/buyers.py

Rules:

Duplicate buyer names are blocked.
Duplicate buyer emails are blocked where email is provided.
Buyer lookup can raise RECORD_NOT_FOUND.
Products

File:

app/services/products.py

Rules:

Duplicate product names are blocked.
Product lookup can raise RECORD_NOT_FOUND.
Counties

File:

app/services/counties.py

Rules:

Duplicate county codes are blocked.
Duplicate county names are blocked.
County lookup can raise RECORD_NOT_FOUND.
Farmer supply

File:

app/services/farmer_supply.py

Rules:

Farmer must exist.
Product must exist.
Quantity must be greater than zero.
Available-until date cannot be earlier than available-from date.
Expected price cannot be negative.
Buyer demand

File:

app/services/buyer_demand.py

Rules:

Buyer must exist.
Product must exist.
Quantity needed must be greater than zero.
Needed-until date cannot be earlier than needed-from date.
Target price cannot be negative.
Tenders

File:

app/services/tenders.py

Rules:

Linked buyer must exist when provided.
Linked product must exist when provided.
Quantity cannot be negative.
Closing date cannot be earlier than opening date.
Source URL must start with http:// or https:// when provided.
Matches

File:

app/services/matches.py

Rules:

A match must reference either buyer_demand_id or tender_id.
A match should not reference both buyer_demand_id and tender_id.
Opportunity score must be between 0 and 100.
Estimated transport cost cannot be negative.
Recommended rule

Do not raise raw exceptions in services for expected business problems.

Avoid this:

raise ValueError("Farmer already exists")

Prefer this:

raise duplicate_record_error(
    entity="Farmer",
    field="phone_number",
    value=farmer_in.phone_number,
)
API behavior

FastAPI catches Sarateal application exceptions centrally.

Registered in:

app/main.py

Using:

register_exception_handlers(app)

This ensures API responses stay consistent.

Dashboard behavior

The Streamlit dashboard currently calls services directly.

This means service exceptions may appear as dashboard errors unless caught in the dashboard layer.

The next improvement should be to update:

dashboard/app.py

so form submissions catch SaratealError and display clean st.error() messages instead of showing stack traces.

Future validation improvements
Short term
Add dashboard-friendly exception display.
Add validation for duplicate supply listings.
Add validation for duplicate demand listings.
Add validation for duplicate tenders from the same source URL.
Add better field normalization for phone numbers and county names.
Medium term
Add update/delete validation.
Add role-based authorization errors.
Add structured audit logging for failed operations.
Add data-source error handling for tender, price, climate, and vegetation feeds.
Long term
Add validation severity levels.
Add machine-readable validation rule IDs.
Add model-risk style validation reports.
Add admin review queues for questionable farmer/buyer records.
Add monitoring for repeated validation failures.
Design standard

Validation should be:

Centralized in structure
Distributed by domain
Consistent in response shape
Human-readable
Machine-readable
Safe for public API use
Useful for dashboards
Ready for future audit trails

This keeps Sarateal simple now, but strong enough to grow into a reliable market-access and food-security intelligence platform.