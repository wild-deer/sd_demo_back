import json
import os
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/market", tags=["market"])

# Define paths to the JSON files
# Using absolute paths as provided in the context
# Calculate the project base directory
# app/routers/ -> app/ -> sd_demo_back/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
FAKE_DATA_DIR = os.path.join(project_root, "fakeData")

SPOT_DATA_DIR = FAKE_DATA_DIR
LONG_TERM_DATA_DIR = FAKE_DATA_DIR

@router.get("/analysis")
async def get_market_analysis(
    trade_type: str = Query(..., alias="type"),
    date: str = Query(...)
):
    try:
        if trade_type == "spot":
            # date format expected: YYYY-MM-DD
            try:
                year, month, day = date.split("-")
                filename = f"现货市场行情{year}年{int(month)}月{int(day)}日.json"
                file_path = os.path.join(SPOT_DATA_DIR, filename)
                print(file_path)
            except ValueError:
                 raise HTTPException(status_code=400, detail="Invalid date format for spot. Expected YYYY-MM-DD")
                
            if not os.path.exists(file_path):
                # Fallback or error? Let's return 404 for now to be clear
                raise HTTPException(status_code=404, detail=f"Spot market data file not found: {filename}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data

        elif trade_type == "long-term":
            # date format expected: YYYY-MM
            try:
                parts = date.split("-")
                if len(parts) >= 2:
                    year, month = parts[0], parts[1]
                    filename = f"中长期时长行情{year}年{int(month)}月.json"
                    file_path = os.path.join(LONG_TERM_DATA_DIR, filename)
                else:
                     raise ValueError
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format for long-term. Expected YYYY-MM")

            if not os.path.exists(file_path):
                 raise HTTPException(status_code=404, detail=f"Long-term market data file not found: {filename}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data

        else:
            raise HTTPException(status_code=400, detail="Invalid trade type")

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
