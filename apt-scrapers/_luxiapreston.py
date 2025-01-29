import requests
import concurrent.futures
import json


id_barrel = "https://inventory.g5marketingcloud.com/graphql"
id_barrel_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://www.luxiapreston.com",
    "priority": "u=1, i",
    "referer": "https://www.luxiapreston.com/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
id_barrel_payload = {
    "query": """query ApartmentComplex($floorplanId: Int, $beds: [Int!], $baths: [Float!], $sqft: Int, $startRate: Int, $endRate: Int, $floorplanGroupId: [Int!], $amenities: [Int!], $locationUrn: String!, $moveInDate: String!, $unitsLimit: Int, $dateFlexibility: Int) {
  apartmentComplex(locationUrn: $locationUrn) {
    id
    showUnits
    showNumberOfAvailableUnits
    showLeaseTerms
    showBestValue
    floorplanGroupDescription
    pricingDisclaimer
    hasAllowableMoveInDays
    hasApartmentSpecials
    hasFloorplanSpecials
    singularUnitLabel
    firstAvailableMoveInDate
    lastAvailableMoveInDate
    availabilityInDays
    brochurePdfLabel
    virtualTourLabel
    floorplans(id: $floorplanId, beds: $beds, baths: $baths, sqft: $sqft, startRate: $startRate, endRate: $endRate, floorplanGroupId: $floorplanGroupId, amenities: $amenities, moveInDate: $moveInDate, dateFlexibility: $dateFlexibility) {
      id
      altId
      externalIds
      name
      totalAvailableUnits
      unitsAvailableByFilters(moveInDate: $moveInDate, dateFlexibility: $dateFlexibility, amenities: $amenities, minPrice: $startRate, maxPrice: $endRate, limit: $unitsLimit)
      allowableMoveInDays
      beds
      baths
      sqft
      sqftDisplay
      rateDisplay
      startingRate
      endingRate
      imageUrl
      imageUrls
      locationCode
      virtualImageUrl
      depositDisplay
      floorplanGroupIds
      brochurePdf
      hasSpecials
      floorplanSpecials {
        id
        name
        __typename
      }
      floorplanAmenities {
        id
        name
        __typename
      }
      floorplanCta {
        name
        url
        actionType
        redirectUrl
        redirectUrlActionType
        ownerType
        vendorKey
        redirectVendorKey
        isExternal
        __typename
      }
      __typename
    }
    floorplanFilters {
      beds
      baths
      sqftMax
      sqftMin
      lastAvailableDate
      floorplanGroups {
        id
        description
        __typename
      }
      amenities {
        id
        name
        __typename
      }
      __typename
    }
    __typename
  }
}
""",
    "variables": {
      "locationUrn": "g5-cl-1okhhuy8m3-cushman-wakefield-fka-pinnacle-plano-tx",
      "moveInDate": "",
      "unitsLimit": 9
    }
}

floorplan_url = "https://inventory.g5marketingcloud.com/graphql"
floorplan_payload = {
    "query": """query Units($floorplanId: Int!, $limit: Int, $moveInDate: String, $locationUrn: String, $altId: String, $amenities: [Int!], $id: Int, $dateFlexibility: Int, $minPrice: Float, $maxPrice: Float) {
  units(floorplanId: $floorplanId, limit: $limit, moveInDate: $moveInDate, locationUrn: $locationUrn, altId: $altId, amenities: $amenities, id: $id, dateFlexibility: $dateFlexibility, minPrice: $minPrice, maxPrice: $maxPrice) {
    id
    externalId
    parentExternalId
    name
    displayName
    building
    sqftDisplay
    availabilityDate
    specials {
      id
      name
      term
      amount
      __typename
    }
    lastAvailableMoveInDate
    prices {
      id
      priceType
      formattedPrice
      value
      __typename
    }
    amenities {
      id
      name
      __typename
    }
    callToActions {
      name
      url
      actionType
      redirectUrl
      redirectUrlActionType
      ownerType
      vendorKey
      redirectVendorKey
      isExternal
      __typename
    }
    __typename
  }
}
""",
    "variables": {
    "locationUrn": "g5-cl-1okhhuy8m3-cushman-wakefield-fka-pinnacle-plano-tx",
    "floorplanId": None,
    "moveInDate": ""
  }
}

def fetch_apartment_data(floorplan_id):
    payload = floorplan_payload.copy()
    payload["variables"]["floorplanId"] = floorplan_id
    response = requests.post(floorplan_url, headers=id_barrel_headers, json=payload)

    if response.status_code == 200:
        return response.json().get("data", {}).get("units", [])
    else:
        print(f"Error fetching data for floorplanId {floorplan_id}: {response.status_code}")
        return []


def luxiapreston():
    response = requests.post(id_barrel, headers=id_barrel_headers, json=id_barrel_payload)
    if response.status_code != 200:
        print(f"Error fetching floorplan IDs: {response.status_code}")
        return

    data = response.json().get("data", {}).get("apartmentComplex", {}).get("floorplans", [])
    floorplan_ids = [floorplan["id"] for floorplan in data]
    print(f"Found {len(floorplan_ids)} floorplan IDs.")

    apartments = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(fetch_apartment_data, floorplan_id): floorplan_id for floorplan_id in floorplan_ids}
        for future in concurrent.futures.as_completed(future_to_id):
            floorplan_id = future_to_id[future]
            try:
                apartments.extend(future.result())
            except Exception as exc:
                print(f"Error fetching data for floorplanId {floorplan_id}: {exc}")

    print(f"Fetched data for {len(apartments)} apartments.")
    
    return apartments
  
if __name__ == "__main__":
  data = luxiapreston()
  print(f"Retrieved {len(data)} records")