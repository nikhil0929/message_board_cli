import requests
import getpass
import json

session = requests.Session()  # Create a Session object

def connect_to_backend(api_url):
    try:
        response = session.get(api_url)
        response.raise_for_status()
        print(f"Connected to {api_url}!")
        return True
    except (requests.HTTPError, requests.ConnectionError) as err:
        print(f"Error occurred: {err}")
        return False

def register_user(api_url):
    print("Please provide the following details for registration:")
    username = input("Username: ")
    password = getpass.getpass("Password: ")  # to hide password
    email = input("Email: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    data = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    headers = {'Content-type': 'application/json'}

    response = session.post(f"{api_url}auth/create/", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("User registered successfully!")
    else:
        print(f"Failed to register user. {response.text}")

def login_user(api_url):
    print("Please provide the following details for login:")
    username = input("Username: ")
    password = getpass.getpass("Password: ")  # to hide password

    data = {
        "username": username,
        "password": password,
    }
    headers = {'Content-type': 'application/json'}

    response = session.post(f"{api_url}auth/login/", data=json.dumps(data), headers=headers)
    print(session.cookies)
    if response.status_code == 200:
        print("User logged in successfully!")
    else:
        print(f"Failed to login. {response.text}")

def create_topic(api_url):
    print("Please provide the following details for new topic:")
    name = input("Topic Name: ")
    description = input("Description: ")

    data = {
        "name": name,
        "description": description
    }
    headers = {'Content-type': 'application/json'}

    response = session.post(f"{api_url}topics/create/", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("Topic created successfully!")
    else:
        print(f"Failed to create topic. {response.text}")

def view_unsubscribed_topics(api_url):
    response = session.get(f"{api_url}topics/list/")
    if response.status_code == 200:
        topics = response.json().get('topics', [])
        print("Unsubscribed topics:")
        for topic in topics:
            print(topic)
    else:
        print(f"Failed to get unsubscribed topics. {response.text}")

def view_subscribed_topics(api_url):
    response = session.get(f"{api_url}topics/subscribed/")
    if response.status_code == 200:
        topics = response.json().get('topics', [])
        print("Subscribed topics:")
        for topic in topics:
            print(topic)
    else:
        print(f"Failed to get subscribed topics. {response.text}")

def subscribe_to_topic(api_url):
    topic_id = input("Enter Topic ID to subscribe to: ")
    response = session.post(f"{api_url}topics/{topic_id}/subscribe/")
    if response.status_code == 200:
        print("Successfully subscribed to topic!")
    else:
        print(f"Failed to subscribe to topic. {response.text}")

def select_topic(api_url):
    view_subscribed_topics(api_url)
    topic_id = input("Enter Topic ID to select: ")
    return topic_id

def get_post_detail(api_url, topic_id):
    post_id = input("Enter Post ID to view details: ")
    response = session.get(f"{api_url}posts/topics/{topic_id}/messages/{post_id}/")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to get post details. {response.text}")

def create_post(api_url, topic_id):
    title = input("Enter your post title: ")
    content = input("Enter your post content: ")

    data = {'title': title, 'content': content}
    headers = {'Content-type': 'application/json'}

    response = session.post(f"{api_url}posts/topics/{topic_id}/messages/create/", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("Post created successfully!")
    else:
        print(f"Failed to create post. {response.text}")

def update_post(api_url, topic_id):
    post_id = input("Enter Post ID to update: ")
    content = input("Enter the new content: ")

    data = {'content': content}
    headers = {'Content-type': 'application/json'}

    response = session.put(f"{api_url}posts/topics/{topic_id}/messages/{post_id}/update/", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("Post updated successfully!")
    else:
        print(f"Failed to update post. {response.text}")

def delete_post(api_url, topic_id):
    post_id = input("Enter Post ID to delete: ")
    response = session.delete(f"{api_url}posts/topics/{topic_id}/messages/{post_id}/delete")
    if response.status_code == 200:
        print("Post deleted successfully!")
    else:
        print(f"Failed to delete post. {response.text}")

def list_posts(api_url, topic_id):
    response = session.get(f"{api_url}posts/topics/{topic_id}/messages/")
    if response.status_code == 200:
        messages = response.json().get('messages', [])
        print("Posts in this topic:")
        for message in messages:
            print(message)
    else:
        print(f"Failed to get posts. {response.text}")

def user_interaction(api_url):
    while True:
        print("\nWelcome! Please select an option: ")
        print("1. Login")
        print("2. Register")
        print("3. Quit")
        option = input("Enter option number: ")

        if option == '1':
            login_user(api_url)
            if 'sessionid' in session.cookies:  # Check if user is logged in
                while True:
                    print("\nSelect an option: ")
                    print("1. Create a topic")
                    print("2. View all your unsubscribed topics")
                    print("3. View your subscribed topics")
                    print("4. Subscribe to a topic")
                    print("5. Select a topic")
                    print("6. Log out")
                    user_option = input("Enter option number: ")

                    if user_option == '1':
                        create_topic(api_url)
                    elif user_option == '2':
                        view_unsubscribed_topics(api_url)
                    elif user_option == '3':
                        view_subscribed_topics(api_url)
                    elif user_option == '4':
                        subscribe_to_topic(api_url)
                    elif user_option == '5':
                        topic_id = select_topic(api_url)
                        while True:
                            print("\nYou have selected a topic. Choose an action: ")
                            print("1. List Posts")
                            print("2. Get Post Detail")
                            print("3. Create Post")
                            print("4. Update Post")
                            print("5. Delete Post")
                            print("6. Back to main menu")
                            topic_option = input("Enter option number: ")

                            if topic_option == '1':
                                list_posts(api_url, topic_id)
                            elif topic_option == '2':
                                get_post_detail(api_url, topic_id)
                            elif topic_option == '3':
                                create_post(api_url, topic_id)
                            elif topic_option == '4':
                                update_post(api_url, topic_id)
                            elif topic_option == '5':
                                delete_post(api_url, topic_id)
                            elif topic_option == '6':
                                print("Returning to main menu...")
                                break
                            else:
                                print("Invalid option. Please select 1, 2, 3, 4, 5 or 6.")
                    elif user_option == '6':
                        print("Logging out...")
                        session.cookies.clear()  # This will log out the user
                        break
                    else:
                        print("Invalid option. Please select 1, 2, 3, 4, 5 or 6.")
        elif option == '2':
            register_user(api_url)
        elif option == '3':
            print("Quitting...")
            break
        else:
            print("Invalid option. Please select 1, 2 or 3.")

if __name__ == "__main__":
    api_url = 'http://messageboard-env.eba-vka44hbw.us-east-2.elasticbeanstalk.com/'  # replace with your Django API URL
    user_interaction(api_url)