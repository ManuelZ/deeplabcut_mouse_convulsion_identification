import cv2
import os


def video_read_write(video_path, start_frame=0, n_frames=30):
    """
    video_path (str): path/to/video
    """
    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        print("Error opening video file")
        return

    video_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if n_frames == "all":
        n_frames = video_frames

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames_per_second = video.get(cv2.CAP_PROP_FPS)
    output_fname = "{}_out.mp4".format(os.path.splitext(video_path)[0])

    output_file = cv2.VideoWriter(
        filename=output_fname,
        fourcc=cv2.VideoWriter_fourcc(*"mp4v"),  # *'MPEG',
        fps=float(frames_per_second),
        frameSize=(width, height),
        isColor=True,
    )

    i = 0
    while video.isOpened() and (i - start_frame) < n_frames:
        print(f"Processing frame {str(i).zfill(3)}", end="\r", flush=True)
        ret, frame = video.read()

        # Stop if there was a problem reading a new video frame
        if not ret:
            print(f"Error reading frame {i}", end="\r", flush=True)
            break

        # Skip until arrive to the desired start frame
        if i < start_frame:
            i += 1
            continue

        # Save frame to new video
        output_file.write(frame)
        i += 1

    print(f"Done. Writing video '{output_fname}'.")
    video.release()
    output_file.release()


def extract_frame(video_path, target_frames):
    """ """

    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        print("Error opening video file")
        return

    i = 0
    while video.isOpened():
        print(f"Processing frame {str(i).zfill(3)}", end="\r", flush=True)
        ret, frame = video.read()

        # Stop if there was a problem reading a new video frame
        if not ret:
            print(f"Error reading frame {i}", end="\r", flush=True)
            break

        # Skip until arrive to the desired start frame
        if i in target_frames:
            cv2.imwrite(f"frame_{i}.jpg", frame)

        i += 1

    video.release()


if __name__ == "__main__":
    video_path = r"cut.mp4"

    # Extract frame of interest
    extract_frame("full_labeled.mp4", [87])

    # Trim video
    # video_read_write(video_path, start_frame=0, n_frames="all")
