import numpy as np

class Lidar_gaps:
    def __init__(self,lidar_data,radius):
        
        self.radius = radius
        self.lidar_data = np.array(lidar_data)

        # Finding the edge lidar points of the objects 
        finite_indices = np.where(np.isfinite(self.lidar_data))[0]
        inf_indices = np.where(np.isinf(self.lidar_data))[0]
        self.edge_indices = np.array([
        idx for idx in finite_indices
        if any(abs(idx - inf_idx) == 1 for inf_idx in inf_indices)
        ])
        
        # Getting an array of the corner points(6 points for 3 objects)
        self.edge_data = self.lidar_data[self.edge_indices] 
        self.x = (self.radius+self.edge_data)*np.cos(self.edge_indices*3.14/180)
        self.y = (self.radius+self.edge_data)*np.sin(self.edge_indices*3.14/180)
        self.edge_points = np.column_stack((self.x,self.y))

        # Grouping the corner points in to 3 groups in order 
        self.edge_grps = self.arrange_data(self.edge_points)

        self.gaps=self.get_gaps()
        

    def euclidean_distance(self,point1, point2):
        """Calculate Euclidean distance between two points."""
        return np.sqrt(np.sum((point1 - point2) ** 2))
    
    def get_gaps(self):
        # print("hi")
        gaps=[None,None,None]
        gaps[0] = self.euclidean_distance(self.edge_grps[0][1],self.edge_grps[1][0])
        gaps[1] = self.euclidean_distance(self.edge_grps[1][1],self.edge_grps[2][0])
        gaps[2] = self.euclidean_distance(self.edge_grps[2][1],self.edge_grps[0][0])
        # print()
        return gaps

    def arrange_data(self,data):
        print(self.euclidean_distance(data[0],data[-1]))
        if self.euclidean_distance(data[0],data[-1]) <= 2.4*self.radius:
        # Move the first element to the back
            # print("rearranged")
            data = np.vstack([data[1:], data[0]])
        
        means = np.mean(data.reshape(3, 2, 2), axis=1)
        distances = np.linalg.norm(means, axis=1)
    
        # Get the indices that would sort the distances
        ranks = np.argsort(-distances)
        
        # Create an array of ranks based on sorted indices
        # print("data:",data)
        grp_arr = [None,None,None]    
        # print(sorted_indices)
        # print(ranks)
        # print(data)
        for rank,i in enumerate(ranks):
            grp_arr[rank] = np.array(data[2*i:2*i+2])
            
        print("grped edges",grp_arr)
        # print("XX==========================XX")
        return grp_arr