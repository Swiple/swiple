import React from 'react';
import { jsonSchema } from './jsonSchema';


export default function ExpectationsList() {
  const jsonSchemaToList = () => {
    return jsonSchema.map((item) => {
      return (
        <div
          key={item.title}
          className="card"
          style={{ marginTop: 16 }}
        >
          <div className="card__header">
            <h3>{item.title}</h3>
          </div>
          <div className="card__body">
            <p>
              {item.description}
            </p>
          </div>
        </div>
      );
    })
  }

  return (
    <section style={{ paddingTop: '4rem', paddingBottom: '4rem'}}>
      <div className="container">
        <div className="row" style={{paddingLeft: 16, marginBottom: 16 }}>
          <h1 style={{ margin: 0, alignSelf: 'flex-end' }}>Expectations</h1>
          <span style={{ fontSize: 18, marginLeft: 20, alignSelf: 'flex-end'}}>{jsonSchema.length} Total</span>
        </div>
        <span>
          Expectations are the assertions executed against your data and are what drive your data quality results.
        </span>
        <div
          className="row"
          style={{
            borderRadius: 8,
            position: 'relative',
            overflow: 'hidden',
            marginTop: 16,
            padding: 16
          }}
        >
          <div
            className="col"
            style={{
              maxHeight: 550,
              overflowY: 'scroll',
              borderRadius: 8,
              paddingBottom: 16,
              background: '#1990ff'
            }}
          >
            {jsonSchemaToList()}
          </div>
        </div>
      </div>
    </section>
  )
}
