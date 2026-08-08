import time
import random

# --- The "Recipe": An efficient data processing function ---
def process_data_item(item_id: int, data: str) -> dict:
    """
    This function represents a well-designed, efficient "recipe" for processing a data item.
    It performs some basic string manipulation and calculation.
    """
    start_time = time.time()
    # A simple, efficient computation that is the 'recipe' itself.
    processed_value = len(data) * (item_id % 10 + 1)
    result = {
        "item_id": item_id,
        "original_data_length": len(data),
        "processed_value": processed_value,
        "status": "success",
        "processing_time_recipe_only": round(time.time() - start_time, 4)
    }
    return result

# --- The "Winter Kitchen Environment": Factors affecting execution ---

# Environment factor 1: Simulated network latency (e.g., slow API calls, database queries)
def simulate_network_latency(min_ms: int = 50, max_ms: int = 300):
    delay = random.randint(min_ms, max_ms) / 1000.0
    # This illustrates how external dependencies (network, DB) can slow down even an efficient recipe.
    time.sleep(delay)
    return delay

# Environment factor 2: Simulated resource contention (e.g., CPU load, memory pressure)
GLOBAL_SYSTEM_LOAD = 0.0 # Can be increased to simulate higher contention
def simulate_resource_contention(base_delay_ms: int = 10):
    global GLOBAL_SYSTEM_LOAD
    # Simulate contention proportional to a global system load
    delay = (base_delay_ms / 1000.0) * (1 + GLOBAL_SYSTEM_LOAD * random.random())
    # Even if the recipe itself is efficient, a busy environment slows it down.
    time.sleep(delay)
    return delay

# Environment factor 3: Simulated intermittent failures (e.g., flaky tests, unexpected errors)
def simulate_intermittent_failure(failure_rate: float = 0.1):
    if random.random() < failure_rate:
        # This shows that even with perfect knowledge (recipe), the environment can cause unexpected issues.
        raise RuntimeError("Simulated intermittent environmental failure!")
    return False # No failure

def run_pipeline(num_items: int, env_config: dict):
    print(f"\n--- Running pipeline with environment config: {env_config['name']} ---")
    total_items_processed = 0
    total_successful = 0
    total_time_taken = 0.0

    # Adjust global load for this run
    global GLOBAL_SYSTEM_LOAD
    GLOBAL_SYSTEM_LOAD = env_config.get('system_load', 0.0)

    for i in range(1, num_items + 1):
        item_data = f"data_for_item_{i}_" * random.randint(5, 15) # Vary data size
        item_id = i
        item_start_time = time.time()
        latency_delay = 0
        contention_delay = 0
        had_failure = False

        try:
            # Apply environmental factors before or during the recipe execution
            if env_config.get('apply_latency'):
                latency_delay = simulate_network_latency(env_config.get('min_latency_ms', 50), env_config.get('max_latency_ms', 300))
            if env_config.get('apply_contention'):
                contention_delay = simulate_resource_contention(env_config.get('base_contention_ms', 10))
            if env_config.get('apply_failure'):
                simulate_intermittent_failure(env_config.get('failure_rate', 0.1))

            # Execute the "recipe" (technical knowledge)
            result = process_data_item(item_id, item_data)
            total_successful += 1
            print(f"  Item {item_id}: SUCCESS. Processed value: {result['processed_value']}. "
                  f"Recipe time: {result['processing_time_recipe_only']:.4f}s. "
                  f"Env delays: Latency={latency_delay:.3f}s, Contention={contention_delay:.3f}s")

        except RuntimeError as e:
            had_failure = True
            print(f"  Item {item_id}: FAILED due to environmental issue: {e}")
        except Exception as e:
            had_failure = True
            print(f"  Item {item_id}: UNEXPECTED ERROR: {e}")
        finally:
            item_end_time = time.time()
            total_time_taken += (item_end_time - item_start_time)
            total_items_processed += 1

    avg_time_per_item = total_time_taken / total_items_processed if total_items_processed > 0 else 0
    print(f"--- Summary for {env_config['name']} ---")
    print(f"Total items attempted: {num_items}")
    print(f"Successfully processed: {total_successful}")
    print(f"Failed items: {num_items - total_successful}")
    print(f"Total time taken: {total_time_taken:.2f}s")
    print(f"Average time per item (including env delays): {avg_time_per_item:.4f}s")
    print("------------------------------------------")


if __name__ == "__main__":
    NUM_ITEMS_TO_PROCESS = 10

    # Scenario 1: Ideal "Winter Kitchen" (minimal environmental impact)
    ideal_env = {
        "name": "Ideal Environment (Good Kitchen)",
        "apply_latency": False,
        "apply_contention": False,
        "apply_failure": False,
        "system_load": 0.0
    }
    run_pipeline(NUM_ITEMS_TO_PROCESS, ideal_env)

    # Scenario 2: "Winter Kitchen" with moderate latency (e.g., external API calls)
    latency_env = {
        "name": "Latency-Affected Environment (Slow Ingredients Delivery)",
        "apply_latency": True,
        "min_latency_ms": 100,
        "max_latency_ms": 500,
        "apply_contention": False,
        "apply_failure": False,
        "system_load": 0.0
    }
    run_pipeline(NUM_ITEMS_TO_PROCESS, latency_env)

    # Scenario 3: "Winter Kitchen" with resource contention (e.g., busy server)
    contention_env = {
        "name": "Contended Environment (Busy Kitchen, Shared Resources)",
        "apply_latency": False,
        "apply_contention": True,
        "base_contention_ms": 50,
        "system_load": 0.5, # Moderate system load
        "apply_failure": False
    }
    run_pipeline(NUM_ITEMS_TO_PROCESS, contention_env)

    # Scenario 4: "Winter Kitchen" with intermittent failures (e.g., flaky infrastructure)
    failure_env = {
        "name": "Flaky Environment (Unreliable Equipment)",
        "apply_latency": False,
        "apply_contention": False,
        "apply_failure": True,
        "failure_rate": 0.2, # 20% chance of failure
        "system_load": 0.0
    }
    run_pipeline(NUM_ITEMS_TO_PROCESS, failure_env)

    # Scenario 5: A combination of challenging environmental factors
    challenging_env = {
        "name": "Challenging Environment (Everything Goes Wrong)",
        "apply_latency": True,
        "min_latency_ms": 200,
        "max_latency_ms": 800,
        "apply_contention": True,
        "base_contention_ms": 100,
        "system_load": 0.8, # High system load
        "apply_failure": True,
        "failure_rate": 0.15 # 15% chance of failure
    }
    run_pipeline(NUM_ITEMS_TO_PROCESS, challenging_env)
