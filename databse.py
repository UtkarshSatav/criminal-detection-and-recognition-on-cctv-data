import requests

def register_face(name, image_path):
    with open(image_path, 'rb') as img:
        response = requests.post(
            "http://localhost:18081/face/register",
            files={"image": img},
            data={"name": name}
        )
        print(response.json())

register_face("Alice", "photos/alice.jpg")
register_face("Bob", "photos/bob.jpg")
