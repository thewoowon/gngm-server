# 길 위에서 만나는 연결, 가는김에

![Pasted Graphic 23](https://github.com/user-attachments/assets/0c399baa-7d8f-424c-8e6e-4d044dc662f1)
![Pasted Graphic 24](https://github.com/user-attachments/assets/eb90df15-3a0f-4355-96dc-0b4976d96453)
![Pasted Graphic 22123](https://github.com/user-attachments/assets/5fd3cb3d-9347-4575-b05a-38884e40bddd)
![Pasted Graphic 21123412](https://github.com/user-attachments/assets/d31121da-aae9-4986-b22a-f6b6bba4fe17)


# API Documentation

## **1. POST /users/**

- **Description**: Create a new user
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
      "message": "User created successfully",
      "user": {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
      }
    }
    ```

## **2. GET /users/**

- **Description**: Retrieve a list of users
- **Query Parameters**:
  - `limit`: Number of users to return (default: 10)
- **Responses**:
  - **200 OK**:
    ```json
    {
      "message": "Returning 10 users"
    }
    ```
