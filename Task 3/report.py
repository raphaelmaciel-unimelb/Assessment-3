try:
    from datetime import datetime, UTC
    import weather as w
    import json
    import statistics as st
    from dotenv import load_dotenv
    from pathlib import Path
    
    load_dotenv()

except (SyntaxError, ImportError, NameError) as synt_err:
     print(f"  [warn] Environment is not ready or Import has failed: {synt_err}")

except Exception as e:
     print(f"  [warn] Environment is not ready or Import has failed: {e}")



def generate_report(log_path, output_path):
    
    return