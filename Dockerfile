# Pull base image
FROM python:3.7-slim

# Copy project
ADD . /FeatureToggleManager 
COPY ./FeatureToggleManager/requirements.txt /FeatureToggleManager/
# Set work directory
WORKDIR /FeatureToggleManager

# Install dependencies
RUN pip install -r requirements.txt

CMD ["python3", "./FeatureToggleManager/manage.py", "runserver", "0.0.0.0:5000"]