import tkinter as tk
import algorithm as algo
import sys
import os
from PIL import ImageGrab
import time
import algo_in_python as algopy


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.clip = False
        self.finish = False
        self.new = True
        self.folder_index = 0
        self.state = 0 # 0 : ear clipping , 1 : optical edge clipping
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=500, height=500, bg="white")
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.pack()

        self.finish_btn = tk.Button(self, text="FINISH", command=self.finish_polygon)
        self.finish_btn.pack(side="left")

        self.redo_btn = tk.Button(self, text="REDO", command=self.redo_polygon)
        self.redo_btn.pack(side="left")

        

        self.clip_btn = tk.Button(self, text="EAR CLIP", command=self.earclip_polygon, fg="red")
        self.clip_btn.pack(side="right")

        self.clip_btn = tk.Button(self, text="OPTIMAL CLIP", command=self.optclip_polygon, fg="green")
        self.clip_btn.pack(side="right")

        self.clip_btn = tk.Button(self, text="SAVE", command=self.save_result, fg="blue")
        self.clip_btn.pack(side="right")

        self.canvas.bind("<Motion>", self.track_mouse)
        self.line = None

        self.not_finish_lb = tk.Label(fg="black", text="Please click the FINISH button first.")
        self.less_than_2_lb = tk.Label(fg="black", text="A polygon must have at least three points.")
        self.save_lb = tk.Label(fg="black", text="Please draw and clip a polygon first.")
        self.intersect_lb = tk.Label(fg="black", text="Polygon is self-intersecting and cannot be triangulated.")

        self.points = []
        self.traingles = []

    def track_mouse(self, event):
        # Only track the mouse if there are points on the canvas already.
        if self.points and self.finish == False and self.clip == False:
            # If there is already a tracking line, remove it.
            if self.line is not None:
                self.canvas.delete(self.line)
            # Draw a new tracking line from the last point to the current mouse position.
            last_point = self.points[-1]
            self.line = self.canvas.create_line(last_point.x, last_point.y, event.x, event.y)

    def add_point(self, event):
        if self.finish == True:
            return 
        if self.clip == True:
            self.points = []
            self.canvas.delete('all')
            self.clip = False
            self.finish = False
            self.clear_label()
            self.new = True
        if self.line is not None:
            self.canvas.delete(self.line)
            self.line = None
        x, y = event.x, event.y
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='black')
        point = algo.Point()
        point.x = x
        point.y = y
        self.points.append(point)

        # Draw a line from the last point to the new one, but only if it's not the first point.
        if len(self.points) > 1:
            last_point = self.points[-2]  # Second to last point.
            self.canvas.create_line(last_point.x, last_point.y, x, y)

    def finish_polygon(self):
        if self.line is not None:
            self.canvas.delete(self.line)
        if len(self.points) > 2:
            if self.less_than_2_lb.winfo_exists():
                self.less_than_2_lb.pack_forget()
                self.update_idletasks()
            x1, y1 = self.points[0].x, self.points[0].y
            x2, y2 = self.points[-1].x, self.points[-1].y
            self.canvas.create_line(x1, y1, x2, y2)
            self.finish = True
        else:
            self.less_than_2_lb.pack()

    def redo_polygon(self):
        self.clear_label()
        self.points = []
        self.canvas.delete('all')
        self.finish = False
        self.clip = False
        self.new = True
        if self.line is not None:
            self.canvas.delete(self.line)
            self.line = None

    def clear_label(self):
        if self.not_finish_lb.winfo_exists():
            self.not_finish_lb.pack_forget()
        if self.intersect_lb.winfo_exists():
            self.intersect_lb.pack_forget()
        if self.less_than_2_lb.winfo_exists():
            self.less_than_2_lb.pack_forget()
        if self.intersect_lb.winfo_exists():
            self.intersect_lb.pack_forget()

    def calculate_signed_area(self):
        area = 0
        n = len(self.points)
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i+1)%n]
            area += (p1.x * p2.y) - (p2.x * p1.y)
        return area / 2

    def ensure_clockwise(self):
        signed_area = self.calculate_signed_area()
        if signed_area < 0:  # If the polygon is counter clockwise
            self.points.append(self.points[0])
            self.points.pop(0)
            self.points.reverse()  # Reverse the order of the points

        return self.points

    def earclip_polygon(self):
        self.clear_label()
        if self.finish == False and self.state == 0:
            self.not_finish_lb.pack()
            self.update_idletasks()
        else:
            self.triangles = []
            self.points = self.ensure_clockwise()

            self.triangles = algo.ear_clipping(self.points)
            # self.triangles = algopy.ear_clipping(self.points)

            if not self.triangles:
                self.intersect_lb.pack()
                self.update_idletasks()
            else:
                self.state = 0
                self.canvas.delete('all')
                for triangle in self.triangles:
                    for i in range(len(triangle)):
                        x1, y1 = triangle[i].x, triangle[i].y
                        x2, y2 = triangle[(i + 1) % len(triangle)].x, triangle[(i + 1) % len(triangle)].y
                        self.canvas.create_line(x1, y1, x2, y2)

                self.save_points = self.points.copy()
            
            self.clip = True
            self.finish = False
            

    def optclip_polygon(self):
        self.clear_label()
        if self.finish == False and self.state == 1:
            self.not_finish_lb.pack()
            self.update_idletasks()
        else:
            self.state = 1
            self.triangles = []
            self.points = self.ensure_clockwise()

            self.triangles = algo.optimal_triangulation(self.points)

            if not self.triangles:
                self.intersect_lb.pack()
                self.update_idletasks()
            else:
                self.canvas.delete('all')
                for triangle in self.triangles:
                    for i in range(len(triangle)):
                        x1, y1 = triangle[i].x, triangle[i].y
                        x2, y2 = triangle[(i + 1) % len(triangle)].x, triangle[(i + 1) % len(triangle)].y
                        self.canvas.create_line(x1, y1, x2, y2)

                self.save_points = self.points.copy()
            # self.points = []
            
            self.clip = True
            self.finish = False

    def save_result(self):
        if self.save_lb.winfo_exists():
            self.save_lb.pack_forget()
        if self.clip == False:
            self.save_lb.pack()
        else:
            self.canvas.update_idletasks()
            # Save the image of clipped polygon
            index = 1
            if self.new == True:
                for folder in sorted(os.listdir("./draw")):
                    if folder == str(index):
                        index += 1
                self.folder_index = index
                os.mkdir("./draw/"+str(self.folder_index))
                self.new = False
            save_path = "./draw/" + str(self.folder_index)
            os.chdir(save_path)
            if self.state == 0:
                save_name = "output_image_ear.png"
                save_triangle = "output_triangle_ear.txt"
            else:
                save_name = "output_image_opt.png"
                save_triangle = "output_triangle_opt.txt"
            print(save_name)
            print(save_path)
            ImageGrab.grab(bbox=(self.canvas.winfo_rootx(),
                        self.canvas.winfo_rooty(),
                        self.canvas.winfo_rootx()+self.canvas.winfo_width(),
                        self.canvas.winfo_rooty()+self.canvas.winfo_height())).save(save_name)

            # Save the input points
            with open('input_point.txt', 'w') as file:
                file.write(str(len(self.save_points)) + '\n')
                for point in self.save_points:
                    file.write(f'{point.x} {point.y}\n')
                self.save_points = []

            # Save the output triangles
            with open(save_triangle, 'w') as file:
                file.write(str(len(self.triangles)) + '\n')
                for triangle in self.triangles:
                    for point in triangle:
                        file.write(f'{point.x} {point.y}\n')
                    file.write('\n')
            os.chdir("../..")

def calculate_signed_area(polygon):
    area = 0
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i+1)%n]
        area += (p1.x * p2.y) - (p2.x * p1.y)
    return area / 2

def ensure_clockwise(polygon):
    signed_area = calculate_signed_area(polygon)
    if signed_area < 0:  # If the polygon is clockwise
        polygon.append(polygon[0])
        polygon.pop(0)
        polygon.reverse()  # Reverse the order of the points

    return polygon

def input_draw():
    root = tk.Tk()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    ww = 600
    wh = 580

    x = (sw-ww) / 2
    y = (sh-wh) / 2
    root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
    root.title("PolyClipper")
    root.resizable(False, False)
    app = Application(master=root)
    app.mainloop()

def input_file():
    state = sys.argv[2]
    for folder in sorted(os.listdir("./file")):
        case_folder=os.path.join("./file",folder)
        print(folder)
        os.chdir(case_folder)
        if os.path.exists("output_point.txt"):
            print("Already have output")
            os.chdir("../..")
            continue
        if os.path.exists("input.txt"):
            with open("input.txt", 'r') as file:
                num_points = int(file.readline().strip())
                # print(num_points)
                polygon = []
                for _ in range(num_points):
                    line = file.readline().strip()
                    x, y = map(int, line.split())
                    point = algo.Point()
                    point.x = x
                    point.y = y
                    polygon.append(point)
            polygon = ensure_clockwise(polygon)
            if state == 'ear':
                # start = time.time()
                triangles = algo.ear_clipping(polygon)
                # end = time.time()
                # print(f"Time for ear clipping algo : {end - start} seconds")

            elif state == 'opt':
                triangles = algo.ear_clipping(polygon)
            else:
                print("Not a valid algo")
            with open('output_point.txt', 'w') as file:
                file.write(str(len(triangles)) + '\n')
                for triangle in triangles:
                    for point in triangle:
                        file.write(f'{point.x} {point.y}\n')
                    file.write('\n')
            os.chdir("../..")
            print("Done")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'file':
        input_file()

    else:
        input_draw()