import numpy as np

class Lidar_Pos:
    def __init__(self,lidar_data,radius):
        self.radius = radius
        self.lidar_data = np.array(lidar_data)
        self.finite_data = self.lidar_data[np.isfinite(self.lidar_data)]
        # print(self.finite_data)
        
        self.finite_indices = np.where(np.isfinite(self.lidar_data))[0]
        # print(self.finite_indices)
        self.x = (self.radius+self.finite_data)*np.cos(self.finite_indices*3.14/180)
        self.y = (self.radius+self.finite_data)*np.sin(self.finite_indices*3.14/180)
        self.points = np.column_stack((self.x,self.y))

    def euclidean_distance(self,point1, point2):
        """Calculate Euclidean distance between two points."""
        return np.sqrt(np.sum((point1 - point2) ** 2))
    
    def forgy_init(self,coordinates,k):
        random_indices = np.random.choice(coordinates.shape[0], k, replace=False)
        random_coordinates = coordinates[random_indices]
        return random_coordinates
    
    def calculate_centroid(self,cluster):
        cluster = np.array(cluster)
        centroid = np.array([np.mean(cluster[:,0]),np.mean(cluster[:,1])])
        # print(centroid)
        return centroid
    
    def k_means_cluster(self,k, points):
        # Initialization: choose k centroids (Forgy, Random Partition, etc.)
        centroids = self.forgy_init(points,k)
        
        # Initialize clusters list
        clusters = [[] for _ in range(k)]
        
        # Loop until convergence
        converged = False
        while not converged:
            # print("1")
            # Clear previous clusters
            clusters = [[] for _ in range(k)]
        
            # Assign each point to the "closest" centroid 
            for point in points:
                distances_to_each_centroid = [self.euclidean_distance(point, centroid) for centroid in centroids]
                cluster_assignment = np.argmin(np.array(distances_to_each_centroid))
                clusters[cluster_assignment].append(point)
            
            # Calculate new centroids
            #   (the standard implementation uses the mean of all points in a
            #     cluster to determine the new centroid)
            new_centroids = [self.calculate_centroid(cluster) for cluster in clusters]
            new_centroids = np.array(new_centroids)
            # print("Centroids:",np.round(centroids,2))
            # print("New Centroids:",np.round(new_centroids,2))
            
            if np.array_equal(centroids,new_centroids):
                converged=True
            
            centroids = new_centroids
            # error = np.mean(np.sum((centroids - new_centroids) ** 2, axis=1))
            
            # if error<0.01:
            #     converged=True
            # print(error)
            if converged:
                return clusters
        

    def pos_estimate(self,k):
        # labels = self.dbscan(self.points,epsilon,min_pts)
        # print("Labels:",labels)
        # grp_1 = self.points[np.where(labels==1)]
        # grp_2 = self.points[np.where(labels==2)]
        # grp_3 = self.points[np.where(labels==3)]
        
        groups = self.k_means_cluster(k,self.points)
        # print(groups)
        p1 = np.mean(np.array(groups[0])[:,0]),np.mean(np.array(groups[0])[:,1])
        p2 = np.mean(np.array(groups[1])[:,0]),np.mean(np.array(groups[1])[:,1])
        p3 = np.mean(np.array(groups[2])[:,0]),np.mean(np.array(groups[2])[:,1])
        pos_estimates = [p1,p2,p3]
        pos_estimates = sorted(pos_estimates, key=lambda point: (point[0]**2 + point[1]**2)**0.5, reverse=True)

        return pos_estimates