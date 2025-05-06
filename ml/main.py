from integration.flow_to_speed import flow_to_speed

if __name__ == "__main__":
    sample_flow = 1000
    speed = flow_to_speed(sample_flow)
    print(f"Estimated speed for {sample_flow} cars: {speed} km/h")
