import config
import numpy as np

class CentroidTracker:
    def __init__(self, max_disappeared=config.MAX_DISAPPEARED):
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.activity_scores = {}  # Dictionary to store activity scores for each object
        self.max_disappeared = max_disappeared

    def register(self, centroid, activity_score=0):  # Accept activity_score as an argument
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.activity_scores[self.next_object_id] = activity_score  # Store activity score
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]
        del self.activity_scores[object_id]  # Remove activity score for the deregistered object

    def update_activity_score(self, object_id, activity_score):
        if object_id in self.objects:
            self.activity_scores[object_id] = activity_score
        else:
            print(f"Object with ID {object_id} not found.")

    def update(self, rects):
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            input_centroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            D = np.linalg.norm(object_centroids - input_centroids[:, np.newaxis], axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                object_id = object_ids[col]
                self.objects[object_id] = input_centroids[row]
                self.disappeared[object_id] = 0

                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    self.register(input_centroids[row])
            else:
                for col in unused_cols:
                    object_id = object_ids[col]
                    self.disappeared[object_id] += 1

                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)

        return self.objects, self.activity_scores  # Return activity scores along with tracked objects
