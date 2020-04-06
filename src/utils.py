# define HSV boundaries (add more over here). 
# Check hsvChart.png
hsv_bounds = [
    ([0, 0, 0], [10, 255, 255]),  # red
    ([11, 0, 0], [35, 255, 255]),  # yellow
    ([36, 0, 0], [70, 255, 255]),  # green
    ([71, 0, 0], [140, 255, 255]),  # blue
    ([141, 0, 0], [179, 255, 255]),  # pink
]

# for each boundary defined in hsv_bounds 
# give a standard color for output in BGR format
single_colors = [(0, 0, 255), (0, 221, 255), (0, 194, 0), (255, 0, 0), (255, 130, 220)]