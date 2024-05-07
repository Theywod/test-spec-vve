import logging

class payload_correction():

    def __init__(self):        
        self.data = []        
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__()')
        self.exposition = 1.0

        self.peak30_target_pos = 100
        self.peak60_target_pos = 200

        self.peak30_pos_func = None
        self.peak60_pos_func = None

    def load_peacs_pos_from_payload(self, filename):
        with open(filename, mode="r", encoding="utf-8") as hello:
            code = hello.read()
        exec(code, globals())

        self.peak30_target_pos = peak1_target_pos
        self.peak60_target_pos = peak2_target_pos
        self.peak30_pos_func = peak1_pos
        self.peak60_pos_func = peak2_pos
        return

    def set_exposition(self, exposition):
        self.exposition = exposition

    def apply(self, spectrum):
        #self.logger.debug("Applying payload correction")
        corrected = [0]*len(spectrum)
        pl = sum(spectrum)

        # Normalizing payload on exposition time
        # Correction function was calculated for payload with exposition time = 1 sec
        pl = pl/self.exposition

        if (pl > 500000):
            pl = 500000
       
        peak1_hpl = self.peak30_target_pos
        peak2_hpl = self.peak60_target_pos
        
        p1 = self.peak30_pos_func(pl)
        p2 = self.peak60_pos_func(pl)
        
        shift1 = p1 - peak1_hpl;
        shift2 = p2 - peak2_hpl;
        
        k1_ = peak1_hpl/(peak1_hpl + shift1);
        k2_ = peak2_hpl/(peak2_hpl + shift2);
        
        k = (k2_ - k1_)/(peak2_hpl - peak1_hpl);
        
        spectr_len = len(spectrum)
        corrected = [0]*spectr_len
        
        # for i in range(0, len(spectrum)):
        #     multiplyer = (i - peak2_hpl)*k + k2_;
        #     new_channel = i*multiplyer
            
        #     integ, frac = divmod(new_channel, 1)
        #     integ = int(integ)
        #     if (integ < (len(spectrum)-1)):          
        #         if (integ > 0):
        #             corrected[integ] = corrected[integ] + spectrum[i]*(1-frac)
        #         corrected[integ+1] = corrected[integ+1] + spectrum[i]*frac    
    
        cursor = -1 # what part of spectrum is transformed
        for i in range(0, spectr_len):
            multiplyer = (i - peak2_hpl)*k + k2_
            new_channel = i*multiplyer 
            channels_diff = new_channel - cursor
        
            h = spectrum[i]
            w = 1
            S = h*w
        
            w_new = channels_diff
            h_new = S/w_new
        
            #integer_part, float_part = divmod(cursor, 1)
            integer_part = int(cursor)
            channel_to_write = int(integer_part+1)        
            if channel_to_write > spectr_len - 1:
                break

            w_portion = channel_to_write - cursor
            if w_portion > w_new:
                w_portion = w_new
        
            w_new = w_new - w_portion
        
            S_portion = w_portion*h_new
            corrected[channel_to_write] = corrected[channel_to_write] + S_portion
            cursor = cursor + w_portion

            while w_new > 0:
                if w_new >= 1:                    
                    int_p = int(cursor + 1)
                    channel_to_write = int(int_p)
                    w_portion = 1
                    cursor = cursor + w_portion
                    w_new = w_new - w_portion
                else:                    
                    int_p = int(cursor+1)
                    channel_to_write = int(int_p)
                    cursor = cursor + w_new
                    w_portion = w_new
                    w_new = 0            
            
                if channel_to_write < spectr_len:
                    S_portion = w_portion*h_new                    
                    corrected[channel_to_write] = corrected[channel_to_write] + S_portion 
                else:
                    break

        return corrected
