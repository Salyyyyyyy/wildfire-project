
class Plot:
    def __init__(self, x, y, terrain, burned_type, severity="moderate"):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.burned_type = burned_type
        self.severity = severity
        self.suggestion = None
        self.cost = 0

    def __str__(self):
        return f"Plot({self.x}, {self.y}) - Terrain: {self.terrain}, Burned: {self.burned_type}, Severity: {self.severity}, Suggestion: {self.suggestion}, Cost: ${self.cost}"

TREE_RULES = {
    "pine": ["hill", "flat"],
    "oak": ["flat", "wetland"],
    "willow": ["wetland"],
    "cedar": ["hill", "rocky"]
}
RECOVERY_COSTS = {
    "replant_pine": 500,
    "replant_oak": 700,
    "replant_willow": 600,
    "replant_cedar": 800,
    "build_shelter": 2000,
    "replant_grass": 200,
    "leave_barren": 0
}
def suggest_recovery(plot):
    if plot.burned_type == "house":
        plot.suggestion = "build_shelter"
    elif plot.burned_type in ["pine", "oak", "willow", "cedar"]:
        if plot.severity == "high":
            plot.suggestion = "replant_grass"
        else:
            for tree, terrains in TREE_RULES.items():
                if plot.terrain in terrains:
                    plot.suggestion = f"replant_{tree}"
                    break
            if plot.suggestion is None:
                plot.suggestion = "replant_grass"
    else:
        plot.suggestion = "leave_barren"

    plot.cost = RECOVERY_COSTS[plot.suggestion]

def get_user_plots():
    plots = []
    num_plots = int(input("How many plots were affected by the wildfire? "))

    for i in range(num_plots):
        print(f"\n--- Plot #{i + 1} ---")
        x = int(input("Enter X coordinate: "))
        y = int(input("Enter Y coordinate: "))
        terrain = input("Enter terrain type (hill, flat, wetland, rocky): ").lower()
        burned_type = input("What burned? (pine, oak, willow, cedar, house, nothing): ").lower()
        severity = input("Fire severity? (low, moderate, high): ").lower()

        plot = Plot(x, y, terrain, burned_type, severity)
        plots.append(plot)

    return plots

def display_grid(plots):
    print("\n📍 AshTracker Recovery Map")
    grid = {}

    for plot in plots:
        key = (plot.x, plot.y)
        grid[key] = plot.suggestion[:2].upper() 

    max_x = max(plot.x for plot in plots)
    max_y = max(plot.y for plot in plots)

    for x in range(max_x + 1):
        row = ""
        for y in range(max_y + 1):
            cell = grid.get((x, y), "  ")
            row += f"[{cell}] "
        print(row)


plots = get_user_plots()

for plot in plots:
    suggest_recovery(plot)

print("\n--- Plot Reports ---")
for plot in plots:
    print(plot)

display_grid(plots)

total_cost = sum(plot.cost for plot in plots)
print(f"\n💰 Total Estimated Recovery Cost: ${total_cost}")
