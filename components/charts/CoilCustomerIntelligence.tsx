'use client'

import { useState } from 'react'

const ROWS = 10

// ─── Proposition 1: Customer Information + Contact Details ───

const prop1CustomerInfoCols = [
  { key: 'name', header: 'Customer / Operator / Asset Owner Name', width: 'min-w-[180px]' },
  { key: 'parent', header: 'Parent Company / Group', width: 'min-w-[150px]' },
  { key: 'country', header: 'Country', width: 'min-w-[100px]' },
  { key: 'region', header: 'Operating Region / Basin / Field', width: 'min-w-[160px]' },
  { key: 'business', header: 'Type of Business (E&P Operator, NOC, IOC, Oilfield, Unconventional)', width: 'min-w-[180px]' },
  { key: 'asset', header: 'Asset Type (Onshore Field, Offshore Platform, Unconventional)', width: 'min-w-[170px]' },
  { key: 'wellType', header: 'Primary Well Type / Application Area (Oil Well, Gas Well...)', width: 'min-w-[170px]' },
  { key: 'provider', header: 'Current Coil Tubing Service Provider / Preferred Vendor', width: 'min-w-[180px]' },
  { key: 'insights', header: 'Other Key Insights (active wells, well depth range, intervention...)', width: 'min-w-[180px]' },
]

const prop1ContactCols = [
  { key: 'contact', header: 'Key Contact Person', width: 'min-w-[130px]' },
  { key: 'designation', header: 'Designation / Role (Well Intervention Manager, Production Manager...)', width: 'min-w-[180px]' },
  { key: 'email', header: 'Email Address', width: 'min-w-[130px]' },
  { key: 'phone', header: 'Phone/WhatsApp Number', width: 'min-w-[140px]' },
  { key: 'linkedin', header: 'LinkedIn Profile', width: 'min-w-[120px]' },
  { key: 'website', header: 'Website URL', width: 'min-w-[120px]' },
]

// ─── Proposition 2 extra: Threat Exposure & Risk Drivers + Purchasing Behaviour ───

const prop2ThreatCols = [
  { key: 'opRisks', header: 'Types of Operational Drivers / Failure Risks (sand production, scale, paraffin...)', width: 'min-w-[200px]' },
  { key: 'incidents', header: 'Past Incidents or Recent Triggers (well decline, NPT event...)', width: 'min-w-[200px]' },
  { key: 'others', header: 'Others (Deferred Production Risk, Well Integrity Risk, HSE)', width: 'min-w-[200px]' },
]

const prop2PurchasingCols = [
  { key: 'decision', header: 'Decision-makers (Well Intervention Head, Production Head, Asset...)', width: 'min-w-[200px]' },
  { key: 'procurement', header: 'Procurement Method (Direct, Tender, Approved Vendor List...)', width: 'min-w-[180px]' },
  { key: 'budget', header: 'Approx. Budget', width: 'min-w-[120px]' },
  { key: 'sourcing', header: 'Current Service Sourcing Model (Single Vendor, Multi...)', width: 'min-w-[180px]' },
  { key: 'buying', header: 'Buying / Contracting Model (Per Job, Campaign-based...)', width: 'min-w-[180px]' },
]

// ─── Proposition 3 extra: Service Requirements + CMI Insights ───

const prop3ServiceCols = [
  { key: 'serviceType', header: 'Type of Coil Tubing Service Required (Well Cleanout, Nitrogen Kickoff, Milling, Fishing...)', width: 'min-w-[220px]' },
  { key: 'intensity', header: 'Service Intensity (Routine, Campaign-based, Shutdown-based, Emergency / Call-out, Production...)', width: 'min-w-[200px]' },
  { key: 'contract', header: 'Preferred Contract Duration (Per Job, Short-term Campaign, 6\u201312 Months, Multi...)', width: 'min-w-[200px]' },
  { key: 'tech', header: 'Technology Expectations (real-time monitoring, digital job reporting, depth...)', width: 'min-w-[200px]' },
  { key: 'compliance', header: 'Compliance & Certification Requirements (HSE, well control, API / ISO, sour service...)', width: 'min-w-[200px]' },
]

const prop3CmiCols = [
  { key: 'benchmarking', header: 'Customer Benchmarking Summary (covers: attractiveness, contract...)', width: 'min-w-[220px]' },
  { key: 'comments', header: 'Additional Comments / Notes by CMI Team (covers: lead priority, pain points...)', width: 'min-w-[220px]' },
]

// ─── Base columns shared by all propositions ───

const baseCols = [...prop1CustomerInfoCols, ...prop1ContactCols]

const baseGroupHeaders = [
  { label: 'Customer Information', span: prop1CustomerInfoCols.length, color: '#FDDBC7' },
  { label: 'Contact Details', span: prop1ContactCols.length, color: '#D4EDDA' },
]

// ─── Generic Table Component ───

function PropositionTable({
  title,
  groupHeaders,
  columns,
  rowCount,
}: {
  title: string
  groupHeaders: { label: string; span: number; color: string }[]
  columns: { key: string; header: string; width: string }[]
  rowCount: number
}) {
  const rows = Array.from({ length: rowCount }, (_, i) => i + 1)

  return (
    <div className="mb-8">
      <h3 className="text-lg font-semibold text-black mb-3">{title}</h3>
      <div className="border rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              {/* Group header row */}
              <tr>
                <th
                  className="px-3 py-2 text-xs font-bold text-black bg-gray-100 border-b border-r text-center"
                  rowSpan={2}
                  style={{ minWidth: '140px' }}
                >
                  Customer Name
                </th>
                {groupHeaders.map((gh, i) => (
                  <th
                    key={i}
                    colSpan={gh.span}
                    className="px-3 py-2 text-xs font-bold text-black border-b border-r text-center"
                    style={{ backgroundColor: gh.color }}
                  >
                    {gh.label}
                  </th>
                ))}
              </tr>
              {/* Column header row */}
              <tr>
                {columns.map((col) => (
                  <th
                    key={col.key}
                    className={`px-3 py-2 text-xs font-semibold text-black bg-gray-50 border-b border-r text-center ${col.width}`}
                  >
                    {col.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((rowNum) => (
                <tr key={rowNum} className="hover:bg-gray-50 border-b">
                  <td className="px-3 py-3 text-center font-medium text-black border-r">
                    Customer {rowNum}
                  </td>
                  {columns.map((col) => (
                    <td
                      key={col.key}
                      className="px-3 py-3 text-center text-black border-r"
                    >
                      xx
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

// ─── Main Component ───

interface CoilCustomerIntelligenceProps {
  height?: number
}

export default function CoilCustomerIntelligence({ height }: CoilCustomerIntelligenceProps) {
  const [activeProposition, setActiveProposition] = useState<1 | 2 | 3>(1)

  return (
    <div style={{ minHeight: height }}>
      <h2 className="text-xl font-bold text-black mb-4">Customer Intelligence</h2>

      {/* Proposition Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-200 pb-2">
        {[1, 2, 3].map((p) => (
          <button
            key={p}
            onClick={() => setActiveProposition(p as 1 | 2 | 3)}
            className={`px-4 py-2 text-sm font-medium rounded-t transition-colors ${
              activeProposition === p
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-black hover:bg-gray-200'
            }`}
          >
            Proposition {p}
          </button>
        ))}
      </div>

      {/* Proposition 1: Customer Information + Contact Details */}
      {activeProposition === 1 && (
        <PropositionTable
          title="Proposition 1 Customer Information & Contact Details"
          groupHeaders={baseGroupHeaders}
          columns={baseCols}
          rowCount={ROWS}
        />
      )}

      {/* Proposition 2: Prop 1 columns + Threat Exposure & Risk Drivers + Purchasing Behaviour */}
      {activeProposition === 2 && (
        <PropositionTable
          title="Proposition 2 Customer Information, Contact Details, Threat Exposure & Purchasing Behaviour"
          groupHeaders={[
            ...baseGroupHeaders,
            { label: 'Threat Exposure & Risk Drivers', span: prop2ThreatCols.length, color: '#D6D8DB' },
            { label: 'Purchasing Behaviour', span: prop2PurchasingCols.length, color: '#C8E6C9' },
          ]}
          columns={[...baseCols, ...prop2ThreatCols, ...prop2PurchasingCols]}
          rowCount={ROWS}
        />
      )}

      {/* Proposition 3: Prop 1 + Prop 2 columns + Service Requirements + CMI Insights */}
      {activeProposition === 3 && (
        <PropositionTable
          title="Proposition 3 Customer Information, Contact Details, Threat Exposure, Purchasing Behaviour, Service Requirements & CMI Insights"
          groupHeaders={[
            ...baseGroupHeaders,
            { label: 'Threat Exposure & Risk Drivers', span: prop2ThreatCols.length, color: '#D6D8DB' },
            { label: 'Purchasing Behaviour', span: prop2PurchasingCols.length, color: '#C8E6C9' },
            { label: 'Service Requirements', span: prop3ServiceCols.length, color: '#FDDBC7' },
            { label: 'CMI Insights', span: prop3CmiCols.length, color: '#C8E6C9' },
          ]}
          columns={[...baseCols, ...prop2ThreatCols, ...prop2PurchasingCols, ...prop3ServiceCols, ...prop3CmiCols]}
          rowCount={ROWS}
        />
      )}
    </div>
  )
}
