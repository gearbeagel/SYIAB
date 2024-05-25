# See Ya In A Bunch

## Personal Time Capsule App

## Overview

"See Ya In A Bunch" is a personal time capsule application designed to capture, store, and revisit memories for future moments. Whether it's a heartfelt message, a cherished photo, a memorable video, or an inspiring audio clip, this app allows users to encapsulate their most precious moments and lock them away until a designated future date. With features like personalized messages, multimedia support, and time capsule sharing, users can preserve their most precious moments and cherish them over time.

## Core Features

1. **User Authentication**: Sign up, log in, and log out securely.
2. **Memory Capturing and Storage**: Capture memories in various forms (text, photos, videos, audio) and securely store them.
3. **Future Date Locking Mechanism**: Lock memories until specified future dates and receive reminders to revisit them.
4. **Customizable Categories for Memories**: Organize memories into custom categories for easy navigation and retrieval.
5. **Multimedia Support**: Playback and interact with multimedia memories, including photos, videos, and audio recordings.

## Project Structure

The project is structured around weekly sprints to implement and enhance the core features. Here's an overview of the weekly tasks:

### Week 1: User Authentication

Implement user registration, login, logout, session management, protected routes, and basic UI for authentication.

### Week 2: Memory Capturing and Storage

Design the database schema for memories, implement memory capturing APIs, integrate media upload support, and ensure seamless backend integration with the UI.

### Week 3: Future Date Locking Mechanism

Develop UI components for setting future date locks, implement backend functionality for locking memories until specified dates, and set up a reminder system for users.

### Week 4: Customizable Memory Categories

Enable users to create custom categories for organizing memories, implement memory tagging and category filtering, and provide management options for custom categories.

### Week 5: Multimedia Support

Enhance support for multimedia memories by developing UI components for media playback, optimizing media storage and compression, and thorough testing of multimedia functionalities.

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/gearbeagel/SYIAB.git
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up database:

    ```
    python manage.py migrate
    ```

4. Start the development server:

    ```
    python manage.py runserver
    ```

5. Access the application:

    Open your web browser and navigate to `http://localhost:8000`.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow the guidelines provided in the repository and submit a pull request with your changes.
