import re

with open('src/app/pages/AccommodationBookingPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the property map block
start_idx = content.find('properties.map(property => {')
end_idx = content.find('{/* Pagination or Load More */}')
old_map = content[start_idx:end_idx]

new_map = """properties.map(property => {
                const isSelected = selectedProperty?.id === property.id;
                return (
                  <div
                    key={property.id}
                    onClick={() => handleCardClick(property)}
                    className={`bg-white rounded-2xl border transition-all duration-300 cursor-pointer flex flex-col sm:flex-row min-h-[220px] overflow-hidden ${
                      isSelected 
                        ? 'border-amber-700 shadow-lg ring-1 ring-amber-700/50' 
                        : 'border-slate-200 hover:border-slate-300 hover:shadow-md'
                    }`}
                  >
                    {/* Thumbnail Image */}
                    <div className="w-full sm:w-2/5 md:w-1/3 h-52 sm:h-auto shrink-0 relative bg-slate-100">
                      <img 
                        src={property.image_url} 
                        alt={property.name}
                        className="absolute inset-0 w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                        onError={(e) => {
                          e.currentTarget.src = "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=400&q=80";
                        }}
                      />
                      <span className="absolute top-3 left-3 bg-black/70 backdrop-blur-sm text-white px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider shadow-sm">
                        {property.type}
                      </span>
                    </div>

                    {/* Meta Details */}
                    <div className="flex-1 p-5 flex flex-col justify-between gap-4 bg-white z-10">
                      <div className="space-y-1">
                        <div className="flex justify-between items-start gap-2">
                          <h3 className="font-bold text-slate-800 text-lg leading-snug">{property.name}</h3>
                          <div className="flex items-center text-amber-500 gap-1 text-xs shrink-0 bg-amber-50 px-2 py-1 rounded-md">
                            <Star className="w-3.5 h-3.5 fill-current" />
                            <span className="font-bold text-amber-900">4.5</span>
                          </div>
                        </div>
                        
                        <p className="text-xs text-slate-500 flex items-center gap-1.5">
                          <MapPin className="w-3.5 h-3.5 text-slate-400" /> {property.distance} km from Temple Entry Gate
                        </p>
                      </div>

                      {/* Amenities Row */}
                      <div className="flex flex-wrap gap-1.5">
                        {property.amenities.slice(0, 4).map((amenity, idx) => (
                          <span key={idx} className="bg-slate-50 border border-slate-100 text-slate-600 rounded px-2 py-1 text-[10px] font-medium flex items-center gap-1">
                            {getAmenityIcon(amenity)} {amenity}
                          </span>
                        ))}
                        {property.amenities.length > 4 && (
                          <span className="text-[10px] text-slate-400 font-bold px-1 mt-1">
                            +{property.amenities.length - 4} more
                          </span>
                        )}
                      </div>

                      {/* Card Footer: Pricing and Book buttons */}
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 border-t border-slate-100 pt-4 mt-auto">
                        <div>
                          <p className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">Starting from</p>
                          <p className="text-xl font-black text-amber-900 font-serif">Rs. {property.price_start}<span className="text-xs text-slate-400 font-sans font-medium"> / night</span></p>
                        </div>
                        <div className="flex gap-2 w-full sm:w-auto">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              openDetails(property);
                            }}
                            className="flex-1 sm:flex-none px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs transition-colors text-center"
                          >
                            Details
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleBookingStart(property);
                            }}
                            className="flex-1 sm:flex-none px-5 py-2.5 bg-amber-800 hover:bg-amber-900 text-white font-bold rounded-xl text-xs transition-all shadow-md hover:shadow-lg active:scale-95 text-center"
                          >
                            Book Now
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          """

content = content.replace(old_map, new_map)

# Ensure the detail modal footer uses items-center, which I might have messed up or they still couldn't see
# Wait, let's make it a prominent button to make it absolutely obvious, and remove any weird shrink-0 that might be hiding it
old_footer = """            {/* Modal Footer */}
            <div className="border-t border-slate-100 p-4 bg-slate-50 flex justify-between items-center shrink-0">
              <a 
                href={`https://www.google.com/search?q=${encodeURIComponent(selectedProperty.name + " Khatu Shyam")}`} 
                target="_blank" 
                rel="noreferrer" 
                className="text-amber-800 text-xs font-bold hover:underline flex items-center gap-1.5"
              >
                View Official Website & Maps
              </a>
              <button
                onClick={() => setDetailModalOpen(false)}
                className="px-5 py-2.5 border border-slate-300 text-slate-700 font-bold rounded-xl text-xs hover:bg-slate-100 transition-colors"
              >
                Close details
              </button>
            </div>"""

new_footer = """            {/* Modal Footer */}
            <div className="border-t border-slate-100 p-4 bg-slate-50 flex flex-col-reverse sm:flex-row justify-between items-center shrink-0 gap-4">
              <a 
                href={`https://www.google.com/search?q=${encodeURIComponent(selectedProperty.name + " Khatu Shyam")}`} 
                target="_blank" 
                rel="noreferrer" 
                className="w-full sm:w-auto px-5 py-2.5 bg-amber-100 hover:bg-amber-200 text-amber-900 text-xs font-bold rounded-xl flex items-center justify-center gap-1.5 transition-colors border border-amber-200"
              >
                <MapPin className="w-3.5 h-3.5" /> View Official Website & Maps
              </a>
              <button
                onClick={() => setDetailModalOpen(false)}
                className="w-full sm:w-auto px-5 py-2.5 border border-slate-300 text-slate-700 font-bold rounded-xl text-xs hover:bg-slate-100 transition-colors text-center"
              >
                Close details
              </button>
            </div>"""

if old_footer in content:
    content = content.replace(old_footer, new_footer)

with open('src/app/pages/AccommodationBookingPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done card update')
