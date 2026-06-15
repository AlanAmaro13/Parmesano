# Create an input file with your queries (one per line)
echo 'Deep Learning Data Augmentation 3D Fossil Reconstruction' > queries.txt

# Run Parmesano
python -m parmesano -i queries.txt -o results.json --max-results 20

# Inspect the results
python -c "
import json
data = json.load(open('results.json'))
s = data['searches'][0]
print(f'Query: {s[\"query\"]}')
print(f'Total indexed: {s[\"total_results\"]:,}')
print(f'Fetched: {s[\"results_fetched\"]}')
print()
for r in s['results']:
    cites = r.get('cited_by', 0)
    print(f'[{cites:>5} cites] {r[\"title\"][:100]}')
    print(f'           {r.get(\"publication_summary\", \"\")}')
    print()
"
