#!/bin/bash

# Title: Termux Installer Script for Auto Update, Python & Firebase Setup
# Author: CyberPrime
# Date: 2024
# Description: This script automates the process of updating/upgrading Termux, installing Python, and required libraries.

echo "----------------------------------------"
echo "Starting Termux update and upgrade process..."
echo "----------------------------------------"

# Update and Upgrade Termux
pkg update -y && pkg upgrade -y

echo "----------------------------------------"
echo "Termux is up-to-date!"
echo "----------------------------------------"

# Install Python
echo "----------------------------------------"
echo "Installing Python..."
echo "----------------------------------------"
pkg install python -y

echo "----------------------------------------"
echo "Python installed successfully!"
echo "----------------------------------------"

# Install Required Python Libraries
echo "----------------------------------------"
echo "Installing required Python libraries..."
echo "----------------------------------------"

# Install pip if not installed already
pip install --upgrade pip

# Install Firebase Admin SDK and other necessary libraries
pip install firebase-admin

echo "----------------------------------------"
echo "Required Python libraries installed!"
echo "----------------------------------------"

# Clean up
echo "----------------------------------------"
echo "Cleaning up Termux..."
echo "----------------------------------------"
pkg autoclean

echo "----------------------------------------"
echo "Setup complete! You can now run your Python scripts with Firebase integration."
echo "----------------------------------------"
