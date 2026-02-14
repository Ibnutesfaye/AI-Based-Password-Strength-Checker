import app
import time

print("--- Testing New Security Features ---")

# 1. Entropy Test
p1 = "password"
p2 = "CorrectHorseBatteryStaple"
p3 = "Tr0ub4dor&3"

print(f"\nEntropy for '{p1}': {app.calculate_entropy(p1):.2f}")
print(f"Entropy for '{p2}': {app.calculate_entropy(p2):.2f}")
print(f"Entropy for '{p3}': {app.calculate_entropy(p3):.2f}")

# 2. HIBP Test (Real API Call)
print("\n--- Testing Have I Been Pwned API ---")
breached_pass = "password123"
safe_pass = "J8#kL9$mN2@pQ5vR" # Random string unlikely to be breached

print(f"Checking '{breached_pass}'...")
count = app.check_pwned_api(breached_pass)
print(f"Result: Found {count} times.")
if count > 0:
    print("✅ HIBP check working (detected breach).")
else:
    print("❌ HIBP check failed (did not detect common password).")

print(f"\nChecking random safe password...")
count_safe = app.check_pwned_api(safe_pass)
print(f"Result: Found {count_safe} times.")
if count_safe == 0:
    print("✅ HIBP check working (correctly identified safe password).")
else:
    print("⚠️ Unexpected: Random password found in breach (or API error).")

# 3. Dynamic Feedback Tes
print("\n--- Testing Dynamic Feedback ---")
# Score 0, Breached
fb = app.get_dynamic_feedback("123456", 0, 1000)
print(f"Feedback for '123456' (Breached): {fb}")

# Score 40, Weak (Short)
fb = app.get_dynamic_feedback("Tr0ub4", 40, 0)
print(f"Feedback for 'Tr0ub4' (Short): {fb}")

# Score 90, Strong
fb = app.get_dynamic_feedback("CorrectHorseBatteryStaple", 90, 0)
print(f"Feedback for 'CorrectHorseBatteryStaple' (Strong): {fb}")

print("\n--- Verification Complete ---")
