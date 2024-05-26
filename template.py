def load_form() -> str:
    return """
        <form action="/submit" method="post">

            <label for="image_url">Docker Image URL:</label><br>
            <input type="text" id="image_url" name="image_url"><br>

            <label for="host_port">Host Port:</label><br>
            <input type="text" id="host_port" name="host_port"><br>

            <label for="container_port">Container Port:</label><br>
            <input type="text" id="container_port" name="container_port"><br>

            <input type="submit" value="Submit">
        </form>
    """
