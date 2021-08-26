<template>
  <b-container class="mt-2">
  <div v-for="item in items" :key="item.product">
    {{ item.product }}
  </div>

  <b>Staff Member</b> <b-form-input v-model="name"></b-form-input>
    <b-table class="mt-4" :items="items" :fields="fields">
      <template #cell(category)="data">
        {{ data.item.category }}
      </template>

      <template #cell(category)="data">
        <span :style="{ 'background-color': background_colour(data.item.category) }">
          <b>{{ data.item.category }}</b>
        </span>
      </template>

      <template #cell(name)="data">
        {{ data.item.name }}
      </template>

      <template #cell(name)="data">
        {{ data.item.name }}
      </template>

      <template #cell(total)="data">
        {{ totals[data.item.name] }}
      </template>
    

      <template #cell()="data">

        <b-form-input
          v-if="data.item[data.field.key] !== false"
          :number=true
          v-model="data.item[data.field.key]"
        />

      </template>
    </b-table>

    <b-button @click="submit" variant="success">
        Submit
    </b-button>
  </b-container>

</template>

<style>
 .table.b-table>thead>tr>th {
  background-color: white;
  position: sticky;
  position: -webkit-sticky;
  top: 0;
  z-index: 2;
} 
</style>

<script>
  import axios from 'axios'

  export default {
    data() {
      const locations = ['fridge', 'display', 'open_table', 'server', 'bench', 'water_fridge' ]
      const colours = {Water: 'lightblue', Mixers: 'red', Beer: 'yellow', 'White Wine': 'green', 'Rose Wine': 'rose', 'Red Wine': 'red', Spirits: 'silver'}
      const products = {
        'Water': 
          {
            'Sparkling large': {fridge: true, water_fridge: true},
            'Sparkling small': {fridge: true, water_fridge: true},
          },
        'Mixers': {
            'Coke': {fridge: true, bench: true},
            'Coke Zero': {fridge: true, bench: true},
            'Lemonade': {fridge: true, bench: true},
            'Soda': {fridge: true, bench: true},
            'Ginger ale': {fridge: true, bench: true},
            'Appletiser': {fridge: true, bench: true},
            'Grapetiser': {fridge: true, bench: true},
            'Lime cordial': {display: true, bench: true},
            'Granadilla cordial': {display: true, bench: true},
        },  
        'Beer': { 
            'Zero to Hero': {fridge: true, bench: true }, 
            'Tafel': {fridge: true, bench: true }, 
            'Striped Horse Lager': {fridge: true, bench: true }, 
            'Jack Black Kegs': {fridge: true}, 
          },

        'White Wine':
          { 
            'Tranquille': {fridge: true, display: true, open_table: true, server: true }, 
            'Force Celeste Semillon': {fridge: true, display: true, open_table: true, server: true }, 
            'Carinus Chenin': {fridge: true, display: true, open_table: true, server: true }, 
          },

        'Rose Wine':
          { 
            'Force Celeste Cinsault Rose': {fridge: true, display: true, open_table: true, server: true }, 
          },
        'Red Wine':
          { 
            'Noble Hill Cruxes': {fridge: true, display: true, open_table: true, server: true }, 
            'Noble Hill Syrah': {display: true, open_table: true, server: true }, 
            'Hell Yeah': {display: true, open_table: true, server: true }, 
          },
        'Spirits':
          { 
            'El Jimedor': {fridge: true, display: true, bench: true}, 
            'Paddys': {display: true, bench: true}, 
            'Sake': {fridge: true, display: true, bench: true}, 
          },
      }

      let counts = []
      for (const category in products) {
       for (const product_name in products[category]) {
          let product = products[category][product_name]
          let this_product = { category: category, name: product_name }
          for(const location of locations) {
            this_product[location] = false
          }
          for(const location in product) {
            this_product[location] = null
          }
          counts.push(this_product)
        }
      }

      return {
        name: '',
        locations: locations,
        items: counts,
        colours: colours,

        fields: [
          { key: 'category', label: 'Category'},
          { key: 'name', label: 'Product'},
          { key: 'fridge', label: 'Fridge Quantity'},
          { key: 'display', label: 'Display Shelf'},
          { key: 'open_table', label: 'Open Wine Area'},
          { key: 'server', label: 'Wine Server'},
          { key: 'bench', label: 'Bench'},
          { key: 'water_fridge', label: 'Water Fridge'},
          { key: 'total', label: 'Total'},
        ],
      }
    },

    computed: {
      totals: function() {
        let totals = {}

        for(const item of this.items) {
          totals[item.name] = 0
          for(const val in item) {
            if(typeof(item[val]) == 'number') {
              totals[item.name] += item[val]
            }
          }
        }
        return totals
      },
    },

    methods: {
      background_colour: function(category) {
        console.log("called fpr", category)
        return this.colours[category]
      },

      submit: function() {
        let counts = JSON.parse(JSON.stringify(this.items))
        for(const item of counts) {
          for(const location of this.locations) {
            if(typeof(item[location]) == 'undefined' || typeof(item[location]) == 'boolean' || item[location] == null ) {
              item[location] = 0
            }
          }
          item['total'] = this.totals[item['name']]
        }
        let submission = {
          counts: counts,
          name: this.name,
          timestamp: Date.now()
        }

        console.log(submission)
        axios.post("http://localhost:5000/", submission).then(response => console.log(response))
      }
    },
  }
</script>