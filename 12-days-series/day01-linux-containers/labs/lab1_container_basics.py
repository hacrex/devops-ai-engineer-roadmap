#!/usr/bin/env python3
"""
Lab 1: Container Basics
Hands-on exercises for Linux Containers fundamentals.

Instructions:
1. Complete each exercise
2. Test your solutions
3. Verify with the success criteria
"""

import subprocess
import sys
import os

# =============================================================================
# EXERCISE 1: Run Your First Container
# =============================================================================


def exercise_1_run_container():
    """
    Task: Run an Alpine Linux container and execute commands inside it.

    Requirements:
    - Pull the alpine:latest image
    - Run a container interactively
    - Execute 'cat /etc/os-release' inside the container
    - Exit the container cleanly

    Success Criteria:
    ✓ Container starts successfully
    ✓ Can view OS information
    ✓ Container exits cleanly (not crashed)

    Hint: Use docker run -it alpine sh
    """

    print("\n" + "=" * 60)
    print("EXERCISE 1: Run Your First Container")
    print("=" * 60)

    # TODO: Write the code to run the container
    # Replace this with your solution
    command = ["docker", "run", "--rm", "alpine", "cat", "/etc/os-release"]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.returncode == 0:
            print("✅ Exercise 1 completed successfully!")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Docker not found. Is Docker installed and running?")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


# =============================================================================
# EXERCISE 2: Build a Custom Image
# =============================================================================


def exercise_2_build_image():
    """
    Task: Create and build a custom Docker image.

    Requirements:
    - Create a Dockerfile that:
      * Uses python:3.11-slim as base
      * Sets working directory to /app
      * Creates a simple Python script that prints "Hello from Container!"
      * Runs the script on container start
    - Build the image with tag "my-hello-app:1.0"
    - Run the container and verify output

    Success Criteria:
    ✓ Dockerfile created with all requirements
    ✓ Image builds without errors
    ✓ Container outputs "Hello from Container!"

    Files to create:
    - Dockerfile
    - app.py (optional, can use RUN echo in Dockerfile)
    """

    print("\n" + "=" * 60)
    print("EXERCISE 2: Build a Custom Image")
    print("=" * 60)

    # TODO: Create Dockerfile
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Create a simple Python script
RUN echo 'print("Hello from Container!")' > app.py

# Run the script
CMD ["python", "app.py"]
"""

    print("Dockerfile content:")
    print(dockerfile_content)

    # Write Dockerfile
    with open("Dockerfile.lab2", "w") as f:
        f.write(dockerfile_content)

    print("\n📄 Dockerfile.lab2 created")

    # TODO: Build the image
    build_command = [
        "docker",
        "build",
        "-t",
        "my-hello-app:1.0",
        "-f",
        "Dockerfile.lab2",
        ".",
    ]

    try:
        print("\nBuilding image...")
        result = subprocess.run(
            build_command, capture_output=True, text=True, timeout=120
        )

        if result.returncode == 0:
            print("✅ Image built successfully!")

            # Run the container
            print("\nRunning container...")
            run_command = ["docker", "run", "--rm", "my-hello-app:1.0"]
            run_result = subprocess.run(
                run_command, capture_output=True, text=True, timeout=30
            )

            print(run_result.stdout)

            if "Hello from Container!" in run_result.stdout:
                print("✅ Exercise 2 completed successfully!")
                return True
            else:
                print("❌ Output doesn't match expected message")
                return False
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


# =============================================================================
# EXERCISE 3: Volume Mounting
# =============================================================================


def exercise_3_volume_mounting():
    """
    Task: Mount a host directory into a container.

    Requirements:
    - Create a directory called 'data' with a file 'message.txt'
    - Run a container that mounts this directory
    - Read the file content from inside the container
    - Modify the file from the container
    - Verify changes persist on host

    Success Criteria:
    ✓ Directory and file created on host
    ✓ Container can read host file
    ✓ Changes made in container persist on host
    ✓ Understand bidirectional sync

    Hint: Use -v $(pwd)/data:/data flag
    """

    print("\n" + "=" * 60)
    print("EXERCISE 3: Volume Mounting")
    print("=" * 60)

    # Create data directory and file
    os.makedirs("data", exist_ok=True)

    with open("data/message.txt", "w") as f:
        f.write("Hello from Host!\n")

    print("✓ Created data/message.txt on host")

    # Read from container
    read_command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{os.getcwd()}/data:/data",
        "alpine",
        "cat",
        "/data/message.txt",
    ]

    try:
        print("\nReading file from container...")
        result = subprocess.run(
            read_command, capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            print(f"Container output: {result.stdout.strip()}")
            print("✓ Container successfully read host file")

            # Write from container
            write_command = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{os.getcwd()}/data:/data",
                "alpine",
                "sh",
                "-c",
                "echo 'Modified by Container' >> /data/message.txt",
            ]

            print("\nModifying file from container...")
            subprocess.run(write_command, capture_output=True, timeout=30)

            # Verify on host
            with open("data/message.txt", "r") as f:
                content = f.read()

            print(f"\nFile content after modification:\n{content}")

            if "Modified by Container" in content:
                print("✅ Exercise 3 completed successfully!")
                print("✓ Changes persisted on host")
                return True
            else:
                print("❌ File wasn't modified correctly")
                return False
        else:
            print(f"❌ Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


# =============================================================================
# EXERCISE 4: Port Mapping
# =============================================================================


def exercise_4_port_mapping():
    """
    Task: Expose a container port to the host.

    Requirements:
    - Run an nginx container with port mapping (8080:80)
    - Verify you can access nginx from host
    - Create a custom HTML page and serve it
    - Access the custom page via browser or curl

    Success Criteria:
    ✓ Container runs with correct port mapping
    ✓ nginx is accessible on localhost:8080
    ✓ Custom HTML page is served
    ✓ Understand host:container port relationship

    Hint: Use -p 8080:80 flag
    """

    print("\n" + "=" * 60)
    print("EXERCISE 4: Port Mapping")
    print("=" * 60)

    # Create custom HTML
    os.makedirs("html", exist_ok=True)

    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>My Container Lab</title>
</head>
<body>
    <h1>Hello from Nginx Container!</h1>
    <p>This page is served from a Docker container.</p>
</body>
</html>
"""

    with open("html/index.html", "w") as f:
        f.write(html_content)

    print("✓ Created custom HTML page")

    # Start nginx container
    container_name = "lab4-nginx"

    # Stop existing container if any
    subprocess.run(
        ["docker", "rm", "-f", container_name], capture_output=True, timeout=10
    )

    run_command = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name,
        "-p",
        "8080:80",
        "-v",
        f"{os.getcwd()}/html:/usr/share/nginx/html",
        "nginx:alpine",
    ]

    try:
        print("\nStarting nginx container...")
        result = subprocess.run(run_command, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✓ Container started")

            # Wait for nginx to start
            import time

            time.sleep(2)

            # Test with curl
            test_command = ["curl", "-s", "http://localhost:8080"]

            print("\nTesting connection...")
            test_result = subprocess.run(
                test_command, capture_output=True, text=True, timeout=10
            )

            if test_result.returncode == 0 and "My Container Lab" in test_result.stdout:
                print("✓ Custom page is accessible")
                print("\n✅ Exercise 4 completed successfully!")
                print(f"\nAccess your page at: http://localhost:8080")

                # Cleanup
                print("\nNote: Container is still running. To stop it:")
                print(f"  docker stop {container_name}")
                print(f"  docker rm {container_name}")

                return True
            else:
                print("❌ Could not access custom page")
                return False
        else:
            print(f"❌ Failed to start container: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


# =============================================================================
# EXERCISE 5: Container Networking
# =============================================================================


def exercise_5_networking():
    """
    Task: Create and use a custom Docker network.

    Requirements:
    - Create a custom bridge network called 'lab-network'
    - Run two containers on this network (e.g., alpine and busybox)
    - Verify they can ping each other by container name
    - Inspect the network to see connected containers

    Success Criteria:
    ✓ Network created successfully
    ✓ Both containers attached to network
    ✓ Containers can communicate by name
    ✓ Understand DNS resolution in Docker networks
    """

    print("\n" + "=" * 60)
    print("EXERCISE 5: Container Networking")
    print("=" * 60)

    network_name = "lab-network"

    # Clean up existing network
    subprocess.run(
        ["docker", "network", "rm", network_name], capture_output=True, timeout=10
    )

    try:
        # Create network
        print("Creating network...")
        create_command = ["docker", "network", "create", network_name]
        result = subprocess.run(
            create_command, capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            print("✓ Network created")

            # Start first container
            print("\nStarting container 1 (web)...")
            subprocess.run(
                ["docker", "rm", "-f", "web"], capture_output=True, timeout=10
            )
            web_command = [
                "docker",
                "run",
                "-d",
                "--name",
                "web",
                "--network",
                network_name,
                "alpine",
                "sleep",
                "300",
            ]
            subprocess.run(web_command, capture_output=True, timeout=30)

            # Start second container
            print("Starting container 2 (api)...")
            subprocess.run(
                ["docker", "rm", "-f", "api"], capture_output=True, timeout=10
            )
            api_command = [
                "docker",
                "run",
                "-d",
                "--name",
                "api",
                "--network",
                network_name,
                "alpine",
                "sleep",
                "300",
            ]
            subprocess.run(api_command, capture_output=True, timeout=30)

            # Test connectivity
            print("\nTesting connectivity from api to web...")
            ping_command = ["docker", "exec", "api", "ping", "-c", "2", "web"]
            ping_result = subprocess.run(
                ping_command, capture_output=True, text=True, timeout=30
            )

            if ping_result.returncode == 0:
                print("✓ Containers can communicate!")
                print(ping_result.stdout)

                # Inspect network
                print("\nNetwork details:")
                inspect_command = ["docker", "network", "inspect", network_name]
                inspect_result = subprocess.run(
                    inspect_command, capture_output=True, text=True, timeout=30
                )

                import json

                network_info = json.loads(inspect_result.stdout)
                containers = network_info[0]["Containers"]

                print(f"\nConnected containers: {len(containers)}")
                for cid, info in containers.items():
                    print(f"  - {info['Name']} ({info['IPv4Address']})")

                print("\n✅ Exercise 5 completed successfully!")

                # Cleanup hint
                print("\nCleanup commands:")
                print("  docker stop web api")
                print("  docker rm web api")
                print(f"  docker network rm {network_name}")

                return True
            else:
                print(f"❌ Connectivity test failed: {ping_result.stderr}")
                return False
        else:
            print(f"❌ Failed to create network: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


# =============================================================================
# MAIN TEST HARNESS
# =============================================================================


def run_all_exercises():
    """Run all lab exercises."""
    print("=" * 60)
    print("CONTAINER BASICS - LAB EXERCISES")
    print("=" * 60)
    print("\nThis lab contains 5 hands-on exercises.")
    print("Complete each exercise to master container fundamentals.\n")

    exercises = [
        ("Exercise 1: Run Container", exercise_1_run_container),
        ("Exercise 2: Build Image", exercise_2_build_image),
        ("Exercise 3: Volume Mounting", exercise_3_volume_mounting),
        ("Exercise 4: Port Mapping", exercise_4_port_mapping),
        ("Exercise 5: Networking", exercise_5_networking),
    ]

    results = []

    for name, func in exercises:
        try:
            result = func()
            results.append((name, result))
        except KeyboardInterrupt:
            print(f"\n⚠️  Interrupted during {name}")
            results.append((name, False))
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("LAB SUMMARY")
    print("=" * 60)

    completed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅ Pass" if result else "❌ Fail"
        print(f"{status} - {name}")

    print(f"\nTotal: {completed}/{total} exercises completed")

    if completed == total:
        print("\n🎉 Congratulations! All exercises passed!")
    else:
        print(f"\n⚠️  {total - completed} exercises need attention. Review and retry.")

    return completed == total


if __name__ == "__main__":
    # Check if Docker is available
    try:
        result = subprocess.run(
            ["docker", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            print("❌ Docker is not installed or not running.")
            print("Please install Docker Desktop or Docker Engine.")
            sys.exit(1)
        print(f"✓ Docker available: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Docker command not found.")
        print("Please install Docker: https://docs.docker.com/get-docker/")
        sys.exit(1)

    # Run exercises
    success = run_all_exercises()
    sys.exit(0 if success else 1)
