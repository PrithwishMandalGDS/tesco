
import pandas as pd
import jinja2
import yaml
import re

excel_file = 'Technical_Contract.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet1', usecols='A')

yaml_lines = []

for cell in df.iloc[:, 0]:
    if pd.notnull(cell):
        cell_lines = str(cell).splitlines()
        yaml_lines.extend(cell_lines)

yaml_content = '\n'.join(yaml_lines)

columns_section_match = re.search(r'columns:(.*?)(?=\ndata_quality_checks:|\Z)', yaml_content, re.DOTALL)

if columns_section_match:
    columns_section = columns_section_match.group(0)
    try:
        parsed_content = yaml.safe_load(columns_section)
        columns = parsed_content.get('columns', {}).get('fields', [])
        for field in columns:
            field['has_enum'] = False
            if 'constraints' in field and field['constraints']:
                for constraint in field['constraints']:
                    if constraint.startswith('ENUM'):
                        field['has_enum'] = True
                        break
    except yaml.YAMLError as e:
        print("Error parsing YAML content:", e)
        columns = []
else:
    print("The 'columns' section was not found in the YAML content.")
    columns = []

template_loader = jinja2.FileSystemLoader(searchpath='./')
env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('ddl_template.j2')

ddl_statement = template.render(fields=columns)

sql_single_line = ' '.join(line.strip() for line in ddl_statement.splitlines() if line.strip())
print(sql_single_line)

output_file = 'dev/raw_on_prem/output.sql'
with open(output_file, 'w') as file:
    file.write(sql_single_line)

print(f"SQL statement written to {output_file}")
