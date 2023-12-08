import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["nimhans"]
#Initialize empty arrays to store fields
chromosomes = []
positions = []
ids = []
refs = []
alts = []
quals = []
filters = []
infos = []
formats = []
samples = []
data_dict = {}
dataHead={}

#Your VCF file path
vcf_file = "samples/H057-301222-ROCHE_S5_R.vcf"
collection =database[vcf_file]

#Open and read the VCF file
with open(vcf_file, "r") as vcf:
    for line in vcf:
        # Skip header lines
        if line.startswith("#"):
            continue

        fields = line.strip().split("\t")
        chromosome, position, vcf_id, ref, alt, qual, filter_val, info, format_val, sample_data = fields

        # Append fields to their respective arrays
        chromosomes.append(chromosome)
        positions.append(position)
        ids.append(vcf_id)
        refs.append(ref)
        alts.append(alt)
        quals.append(qual)
        filters.append(filter_val)
        infos.append(info)
        formats.append(format_val)
        samples.append(sample_data)



#Print or manipulate the arrays as needed
for i in range(len(chromosomes)):
    #print(f"Chromosome: {chromosomes[i]}, Position: {positions[i]}, ID: {ids[i]}, REF: {refs[i]}, ALT: {alts[i]}, QUAL: {quals[i]}, FILTER: {filters[i]}")
    dataHead={'Chromosome': chromosomes[i], 'Position': positions[i], 'ID': ids[i], 'REF':refs[i], 'ALT': alts[i], 'QUAL':quals[i], 'FILTER': filters[i]}
    #for j in range(len(info[i])
    print(dataHead)

#Split the data into individual fields based on semicolon (;)
    data_fields = infos[i].split(";")

#Loop through the data fields and add them to the dictionary
    for field in data_fields:
        key, value = field.split("=")
        data_dict[key] = value


#Print the resulting dictionary
    print(data_dict)
    dataHead['INFO'] = data_dict
    print("\n")

    format_fields = formats[i].split(":")
    format_data = {field: value for field, value in zip(format_fields, sample_data.split(":"))}
    print(format_data)
    dataHead['FORMAT'] = format_data
    print("\n")
    collection.insert_one(dataHead)
'''    
    header, values = formats[i].split(" ", 1)
    format_fields = header.split(":")
    format_values = values.split(":")
    format_data = {field: value for field, value in zip(format_fields, format_values)}
    print(format_data)
'''