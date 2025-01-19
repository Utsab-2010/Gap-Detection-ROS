import numpy as np

class Lidar_Pos:
    def __init__(self,lidar_data,radius):
        self.radius = radius
        self.lidar_data = np.array(lidar_data)
        finite_indices = np.where(np.isfinite(self.lidar_data))[0]
        inf_indices = np.where(np.isinf(self.lidar_data))[0]
        # print(self.finite_data)
        # self.edge_indices = np.array([])
        # print(self.lidar_data)
        # print(finite_indices)
        self.edge_indices = np.array([
        idx for idx in finite_indices
        if any(abs(idx - inf_idx) == 1 for inf_idx in inf_indices)
        ])
        
        # print(self.edge_indices)
        self.edge_data = self.lidar_data[self.edge_indices] 
        # print(self.finite_indices)
        self.x = (self.radius+self.edge_data)*np.cos(self.edge_indices*3.14/180)
        self.y = (self.radius+self.edge_data)*np.sin(self.edge_indices*3.14/180)
        self.edge_points = np.column_stack((self.x,self.y))

        self.edge_grps = self.arrange_data(self.edge_points)

    def euclidean_distance(self,point1, point2):
        """Calculate Euclidean distance between two points."""
        return np.sqrt(np.sum((point1 - point2) ** 2))
    
    def arrange_data(self,data):
        print(self.euclidean_distance(data[0],data[-1]))
        if self.euclidean_distance(data[0],data[-1]) <= 2.4*self.radius:
        # Move the first element to the back
            print("rearranged")
            data = np.vstack((data[1:], data[0]))
        
        means = np.mean(data.reshape(3, 2, 2), axis=1)
        distances = np.linalg.norm(means, axis=1)
    
        # Get the indices that would sort the distances
        ranks = np.argsort(-distances)
        
        # Create an array of ranks based on sorted indices
        
        grp_arr = [None,None,None]    
        # print(sorted_indices)
        print(ranks)
        print(data)
        for rank,i in enumerate(ranks):
            grp_arr[rank] = np.array([data[2*i:2*i+2]])
            
        print(grp_arr)
        print("XX==========================XX")
        return grp_arr