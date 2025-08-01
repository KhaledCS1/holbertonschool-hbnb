# HBnB Frontend Client (Part 4)

## Overview

Part 4 of the HBnB project implements the frontend client interface. It uses HTML5, CSS3, and vanilla JavaScript (ES6) to interact with the backend API (Part 3). The client provides core user flows: authentication, listing places, filtering by price, viewing place details, and adding reviews.

## Features

* **Login**: Authenticate users via JWT tokens stored in cookies.
* **Places List**: Fetch and render a list of places in card format.
* **Client-Side Filtering**: Filter visible places by maximum price (\$10, \$50, \$100, or All) without page reload.
* **Place Details**: Display name, description, location, price, amenities, and existing reviews.
* **Add Review**: Authenticated users can submit reviews and ratings via an AJAX form.

## Technology Stack

* **HTML5**: Semantic markup for pages.
* **CSS3**: Responsive styling (styles.css).
* **JavaScript (ES6)**: Fetch API, DOM manipulation (scripts.js).
* **Static Server**: Python’s built-in HTTP server for serving static files.

## Setup and Run

1. **Ensure Backend API** (Part 3) is running on `http://localhost:5000`.
2. **Serve Frontend**:

   ```bash
   cd part4/base_files
   python3 -m http.server 8000
   ```
3. **Access Pages** in a browser at:

   * `http://localhost:8000/login.html`
   * `http://localhost:8000/index.html`
   * `http://localhost:8000/place.html?id=<PLACE_ID>`
   * `http://localhost:8000/add_review.html?id=<PLACE_ID>`

> Note: Use a modern browser; do not open files with `file://`. The server port must match the one configured in scripts.js.

## Directory Structure (Part 4)

```
part4/base_files/
├── index.html       # Main listing page
├── login.html       # Authentication page
├── place.html       # Detailed place view
├── add_review.html  # Review submission form
├── styles.css       # Global and component styles
└── scripts.js       # Fetch API calls and UI logic
```

## Usage Flow

1. **Login**: Visit `login.html`, enter credentials, submit form.
2. **Places Listing**: After login, `index.html` auto-loads place cards.
3. **Filter**: Select a max price to hide cards above that value.
4. **Details**: Click “View Details” to open `place.html?id=…`.
5. **Add Review**: On details page, fill and submit the review form.

## Contributing

* Fork this repository and work in `part4/base_files`.
* Open an issue or create a feature branch for enhancements.
* Submit a pull request against `main` when ready.


