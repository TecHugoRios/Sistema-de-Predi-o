
use('AquaSpyDB');
db.getCollection('wastedata2000to2019')
  .find(
    {
     'entity':'Europe'
    })
