// mockApi.js - Provides mock API responses when backend is not available

// Mock debate data
const mockDebates = {
  "debate-1": {
    status: "ready",
    current_speaker_index: 0,
    total_speakers: 8,
    config: {
      motion: "This house would legalize marijuana",
      roles: [
        { role: "Prime Minister", is_human: false, nickname: "AI" },
        { role: "Leader of Opposition", is_human: true, nickname: "User" },
        { role: "Deputy Prime Minister", is_human: false, nickname: "AI" },
        { role: "Deputy Leader of Opposition", is_human: false, nickname: "AI" },
        { role: "Member of Government", is_human: false, nickname: "AI" },
        { role: "Member of Opposition", is_human: false, nickname: "AI" },
        { role: "Government Whip", is_human: false, nickname: "AI" },
        { role: "Opposition Whip", is_human: false, nickname: "AI" }
      ]
    },
    speech_log: [],
    speaker_info: []
  }
};

// Mock AI speeches for different roles
const mockAISpeeches = {
  "Prime Minister": 
    "Thank you, Mr. Speaker. Today, I rise to propose that this house would legalize marijuana. This is not merely a question of personal freedom, but one of public health, economic opportunity, and social justice.\n\nFirst, let's consider the medical benefits. Cannabis has proven therapeutic properties for conditions ranging from chronic pain to epilepsy. Legalization would facilitate research and ensure patients have safe, regulated access.\n\nSecond, prohibition has failed. Despite billions spent on enforcement, marijuana remains widely available. Meanwhile, criminal organizations profit enormously. Legalization would redirect these funds to legitimate businesses, creating jobs and tax revenue.\n\nThird, current policies disproportionately impact marginalized communities. Black and brown citizens face higher arrest rates despite similar usage patterns across demographics. Legalization would begin to address this injustice.\n\nFinally, regulation allows for quality control, preventing contamination with harmful substances and ensuring appropriate age restrictions.\n\nI urge the house to support this motion and embrace a more rational, evidence-based approach to cannabis policy.",
  
  "Leader of Opposition": 
    "Thank you, Mr. Speaker. The government today proposes marijuana legalization with appealing rhetoric about freedom and justice, but their case fundamentally misunderstands the serious public health implications.\n\nFirst, cannabis is not the harmless substance the government portrays. Studies link regular use to mental health issues including psychosis and schizophrenia, particularly in young people with developing brains. Legalization sends a dangerous message that this drug is safe.\n\nSecond, the government's economic arguments are shortsighted. While they focus on tax revenue, they ignore the substantial healthcare and productivity costs that would follow increased usage rates—costs we've seen in regions that have legalized.\n\nThird, their social justice argument is flawed. We can address discriminatory enforcement without full legalization. Decriminalization would remove criminal penalties while maintaining necessary restrictions.\n\nFinally, the government ignores the practical challenges of regulation. From impaired driving to workplace safety, legalization creates complex problems without clear solutions.\n\nThis house should reject this reckless proposal and instead pursue evidence-based drug policies that truly protect public health and safety.",
  
  "Deputy Prime Minister":
    "Thank you, Mr. Speaker. The Leader of Opposition has presented concerns that, while understandable, are fundamentally misguided and contradict the evidence.\n\nOn public health, the Opposition's argument actually supports our case. Under prohibition, cannabis is unregulated, untested, and potentially dangerous. Legalization enables quality control, proper labeling, and education campaigns—all proven to reduce harm. The Opposition's fear-mongering about mental health ignores that these risks exist regardless of legal status, and are best addressed through regulation.\n\nRegarding economic impact, the Opposition's cost projections are speculative and contradicted by real-world evidence. Colorado generated over $387 million in tax revenue in 2020 alone, funding education and public health programs. Meanwhile, enforcement costs plummeted.\n\nOn social justice, the Opposition's proposed decriminalization is half-measured. It leaves supply in criminal hands while failing to address the lasting consequences of criminal records that devastate communities.\n\nFinally, the practical challenges the Opposition raises are precisely why we need comprehensive regulation rather than the current failed approach.\n\nThis house should support legalization as the evidence-based, pragmatic solution to cannabis policy.",
  
  "Deputy Leader of Opposition":
    "Thank you, Mr. Speaker. The Government's case continues to rest on false premises and misleading claims that don't withstand scrutiny.\n\nFirst, regarding regulation, the Deputy Prime Minister suggests legalization ensures safety, yet evidence from legalized markets shows concerning trends. High-potency products with THC concentrations exceeding 90% have emerged, far stronger than traditional cannabis and with unknown long-term effects. The profit motive drives companies to create increasingly potent and addictive products, just as we've seen with tobacco and alcohol.\n\nSecond, on economics, the Government cherry-picks revenue figures while ignoring comprehensive cost-benefit analyses. A Canadian study found that for every dollar gained in tax revenue, society incurs nearly two dollars in health, safety, and productivity costs.\n\nThird, regarding social justice, we agree reform is needed, but legalization creates new inequities. Corporate interests, predominantly white-owned, now profit from an industry that previously led to incarceration for marginalized communities.\n\nFinally, the Government has no credible plan for preventing youth access or addressing impaired driving—critical public safety concerns that remain unsolved in legalized markets.\n\nThis house should reject this flawed proposal and pursue more balanced, evidence-based reforms.",
  
  "Member of Government":
    "Thank you, Mr. Speaker. As the first speaker for the Closing Government, I'll address key issues raised in this debate while introducing crucial new material.\n\nThe Opposition has consistently mischaracterized the relationship between legalization and harm. Their argument assumes that prohibition reduces use and harm, yet Portugal's experience with drug decriminalization demonstrates the opposite—when coupled with public health approaches, liberalization reduces problematic use and harm.\n\nI'd like to introduce a new dimension: international relations. Current prohibition empowers cartels and destabilizes producer countries. Mexico alone has seen over 150,000 murders linked to drug trafficking. Legalization would undermine these criminal enterprises and support regional stability.\n\nFurthermore, the Opposition's concerns about corporate capture can be addressed through thoughtful regulation—including caps on market share, support for small producers, and community reinvestment requirements. These approaches have been successfully implemented in states like Illinois.\n\nFinally, regarding impaired driving, evidence from legalized jurisdictions shows no significant increase in traffic fatalities. Modern testing methods and public education campaigns effectively address this concern.\n\nThis house should support legalization as a comprehensive solution to the failures of prohibition.",
  
  "Member of Opposition":
    "Thank you, Mr. Speaker. As the first speaker for Closing Opposition, I'll address the Government's arguments while introducing critical new considerations they've overlooked.\n\nThe Government's international relations argument actually undermines their case. Unilateral legalization would violate international drug control treaties, creating diplomatic tensions and potentially trade repercussions. A more coordinated international approach is necessary.\n\nI introduce a new argument regarding environmental impact. Commercial cannabis production is extraordinarily resource-intensive, consuming massive amounts of water and energy. In California, legal cultivation has caused watershed damage and forest fragmentation. Without addressing these impacts, legalization represents an environmental threat.\n\nFurthermore, the Government has ignored the workplace safety implications. Unlike alcohol, THC remains detectable for weeks after use, creating significant challenges for safety-sensitive industries. No reliable test currently exists to accurately measure impairment.\n\nFinally, the Government's regulatory optimism is naive. The tobacco and alcohol industries demonstrate how commercial interests inevitably undermine public health regulations through lobbying, marketing, and political influence.\n\nThis house should reject this shortsighted proposal and instead pursue comprehensive reform that addresses these complex realities.",
  
  "Government Whip":
    "Thank you, Mr. Speaker. As Government Whip, I'll summarize this debate and crystallize why legalization represents the most rational, evidence-based approach to cannabis policy.\n\nThroughout this debate, our side has demonstrated that prohibition has comprehensively failed its stated objectives. Cannabis remains widely available, criminal organizations profit enormously, and enforcement disproportionately targets marginalized communities. Meanwhile, patients struggle to access beneficial medical treatments.\n\nWe've shown that legalization, properly implemented, addresses these failures through regulated production, age restrictions, quality control, taxation, and public education. The Opposition's concerns—from mental health to impaired driving—are best addressed through regulation, not prohibition.\n\nThe Opposition has offered no viable alternative. Their suggested decriminalization maintains the criminal supply chain while failing to capture the economic and regulatory benefits of legalization.\n\nUltimately, this debate reflects two approaches: the Government's evidence-based, pragmatic policy versus the Opposition's fear-driven defense of a failed status quo. The choice is clear.\n\nThis house should support cannabis legalization as the rational path forward, aligning policy with evidence rather than outdated moral panic.",
  
  "Opposition Whip":
    "Thank you, Mr. Speaker. As Opposition Whip, I'll summarize why the Government's proposal for cannabis legalization fails to serve the public interest.\n\nThroughout this debate, we've demonstrated that legalization creates significant public health risks, particularly for young people and vulnerable populations. The Government's regulatory optimism ignores the reality that commercialization inevitably prioritizes profit over health.\n\nWe've shown that the economic case is fundamentally flawed, failing to account for healthcare costs, workplace impacts, and enforcement challenges that would accompany legalization.\n\nWe've highlighted that the Government's social justice arguments are undermined by the reality of corporate capture and new forms of inequality that emerge in legalized markets.\n\nFinally, we've demonstrated that the Government has no credible solutions for the environmental impacts, international treaty obligations, or workplace safety challenges their policy would create.\n\nThe Opposition has consistently advocated for evidence-based reform that addresses enforcement inequities without embracing full commercialization. Decriminalization, expanded research, and targeted medical access represent a more balanced approach.\n\nThis house should reject this flawed proposal and pursue thoughtful, incremental reform that truly protects public health and safety."
};

// Mock API functions
export const mockApi = {
  // Start a new debate
  startDebate: async (config) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const debateId = "debate-1";
        mockDebates[debateId] = {
          status: "initializing",
          current_speaker_index: 0,
          total_speakers: config.roles.length,
          config: config,
          motion: config.motion, // Store the motion explicitly
          speech_log: [],
          speaker_info: []
        };
        
        console.log("Debate started with motion:", config.motion);
        
        // Simulate initialization delay
        setTimeout(() => {
          mockDebates[debateId].status = "ready";
        }, 3000);
        
        resolve({ debate_id: debateId, status: "initializing" });
      }, 1000);
    });
  },
  
  // Get debate status
  getDebateStatus: async (debateId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const debate = mockDebates[debateId];
        if (!debate) {
          throw new Error("Debate not found");
        }
        
        resolve({
          status: debate.status,
          current_speaker_index: debate.current_speaker_index,
          total_speakers: debate.total_speakers,
          current_speaker: debate.config.roles[debate.current_speaker_index]?.role,
          speech_log_length: debate.speech_log.length
        });
      }, 500);
    });
  },
  
  // Get next speaker
  getNextSpeaker: async (debateId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const debate = mockDebates[debateId];
        if (!debate) {
          throw new Error("Debate not found");
        }
        
        if (debate.current_speaker_index >= debate.config.roles.length) {
          resolve({ status: "complete", message: "Debate is complete" });
          return;
        }
        
        const currentRole = debate.config.roles[debate.current_speaker_index];
        resolve({
          role: currentRole.role,
          is_human: currentRole.is_human,
          nickname: currentRole.nickname,
          index: debate.current_speaker_index,
          total: debate.config.roles.length
        });
      }, 500);
    });
  },
  
  // Submit speech
  submitSpeech: async (debateId, speechInput) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const debate = mockDebates[debateId];
        if (!debate) {
          throw new Error("Debate not found");
        }
        
        const currentIndex = debate.current_speaker_index;
        if (currentIndex >= debate.config.roles.length) {
          throw new Error("Debate is already complete");
        }
        
        const currentRole = debate.config.roles[currentIndex];
        if (speechInput.role !== currentRole.role) {
          throw new Error(`Expected speech from ${currentRole.role}, got ${speechInput.role}`);
        }
        
        // Add speech to log
        debate.speech_log.push(speechInput.text);
        debate.speaker_info.push({
          role: currentRole.role,
          speaker: currentRole.nickname || (currentRole.is_human ? "Human" : "AI")
        });
        
        // Move to next speaker
        debate.current_speaker_index += 1;
        
        resolve({ status: "success", speech_text: speechInput.text });
      }, 1000);
    });
  },
  
  // Generate AI speech
  generateAISpeech: async (debateId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const debate = mockDebates[debateId];
        if (!debate) {
          throw new Error("Debate not found");
        }
        
        const currentIndex = debate.current_speaker_index;
        if (currentIndex >= debate.config.roles.length) {
          throw new Error("Debate is already complete");
        }
        
        const currentRole = debate.config.roles[currentIndex];
        if (currentRole.is_human) {
          throw new Error("Current speaker is human, not AI");
        }
        
        // Generate AI speech with delay to simulate processing
        setTimeout(() => {
          // Get speech based on the role and motion
          const speech = mockAISpeeches[currentRole.role];
          
          // Add speech to log
          debate.speech_log.push(speech);
          debate.speaker_info.push({
            role: currentRole.role,
            speaker: "AI"
          });
          
          // Move to next speaker
          debate.current_speaker_index += 1;
          
          // Play the speech using Web Speech API
          if (window.speechSynthesis) {
            const utterance = new SpeechSynthesisUtterance(speech);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            
            // Try to get a good voice
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
              voice.name.includes('English') && 
              (voice.name.includes('Male') || voice.name.includes('UK'))
            );
            
            if (preferredVoice) {
              utterance.voice = preferredVoice;
            }
            
            window.speechSynthesis.speak(utterance);
          }
        }, 3000);
        
        resolve({ status: "generating", role: currentRole.role });
      }, 500);
    });
  },
  
  // Get all speeches
  getSpeeches: async (debateId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const debate = mockDebates[debateId];
        if (!debate) {
          throw new Error("Debate not found");
        }
        
        const speeches = debate.speech_log.map((speech, i) => {
          const speakerInfo = debate.speaker_info[i] || { role: "Unknown", speaker: "Unknown" };
          return {
            role: speakerInfo.role,
            speaker: speakerInfo.speaker,
            speech: speech,
            index: i
          };
        });
        
        resolve(speeches);
      }, 500);
    });
  },
  
  // Process audio (mock)
  processAudio: async (audioBase64) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // Simulate speech-to-text processing
        resolve({ 
          text: "This is a transcription of your speech. In a real implementation, this would be the result of processing your audio recording through a speech-to-text service. For this demo, we're providing this placeholder text to simulate the functionality." 
        });
      }, 2000);
    });
  }
};

export default mockApi;
